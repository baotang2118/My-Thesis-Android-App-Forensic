import sys
import os
import time
import argparse
from datetime import datetime, timedelta
import cmd_databases
import analyze_43
import android_analysis_17
import random
from threading import Timer
from subprocess import Popen, PIPE, STDOUT
from subprocess import call


# Get argurments
parser = argparse.ArgumentParser(description='Android application forensic')
parser.add_argument('--input', type=str, help='Input raw image (img, iso, dd)')
parser.add_argument('--fastmode', type=str, help='Use fastmode when searching the name of folder in file, only .java, .xml and .json are used')
parser.add_argument('--min_length', type=str, help='minimum name of directory\'s length')
args = parser.parse_args()

# Define tool
if args.input:
    raw_img = args.input
else:
    # raw_img = "E:\\raw_hard_disk\\youware_old.img"
    # raw_img = "E:\\raw_hard_disk\\youwave_vm01.img"
    # raw_img = "E:\\raw_hard_disk\\A80_GooglePixel_2.dd"
    raw_img = "E:\\raw_hard_disk\\SamsungGalaxyS8_Android7.dd"


img_stat = "..\\sleuthkit\\bin\\img_stat.exe "
mmls = "..\\sleuthkit\\bin\\mmls.exe "
fls = "..\\sleuthkit\\bin\\fls.exe "
icat = "..\\sleuthkit\\bin\\icat.exe "
tsk_recover = "..\\sleuthkit\\bin\\tsk_recover.exe "

jadx = "..\\jadx-1.0.0\\bin\\jadx.bat "

report_img_stat = "..\\tmp\\img_stat.txt"
report_mmls = "..\\tmp\\mmls.txt"
report_fls = "..\\tmp\\fls.txt"

source_obj_id = "..\\tmp\\source_obj_id.txt"
part_obj_id = "..\\tmp\\part_obj_id.txt"
object_obj_id = "..\\tmp\\object_obj_id.txt"


# check the exist of image
def check_raw_img_exist():
    if not os.path.exists(raw_img):
        sys.exit("Lack of raw_img!")


# check the temporary file
def check_tmp_exist():
    if not os.path.exists(source_obj_id):
        f = open(source_obj_id, "w")
        f.write('0')
        f.close()
    if not os.path.exists(part_obj_id):
        f = open(part_obj_id, "w")
        f.write('0')
        f.close()
    if not os.path.exists(object_obj_id):
        f = open(object_obj_id, "w")
        f.write('0')
        f.close()


# check complete tools
def check_tools_exist():
    if not os.path.exists(img_stat):
        sys.exit("img_stat is required!")
    if not os.path.exists(mmls):
        sys.exit("mmls is required!")
    if not os.path.exists(fls):
        sys.exit("fls is required!")
    if not os.path.exists(icat):
        sys.exit("icat is required!")
    if not os.path.exists(tsk_recover):
        sys.exit("tsk_recover is required!")
    if not os.path.exists(jadx):
        sys.exit("jadx is required!")


# Search for the image type, image size and sector size
def run_img_stat():
    Image_Type = None
    Size_in_bytes = None
    Sector_size = None

    cmd = img_stat + raw_img
    cmd += " > "
    cmd += report_img_stat
    # print (cmd)
    os.system(cmd)
    f = open(report_img_stat, "r")
    for i in f:
        if "Image Type:" in i:
            splited_contents = i.split(" ")
            Image_Type = splited_contents[-1].strip()

        if "Size in bytes:" in i:
            splited_contents = i.split(" ")
            Size_in_bytes = splited_contents[-1].strip()

        if "Sector size:" in i:
            splited_contents = i.split("\t")
            Sector_size = splited_contents[-1].strip()

    f.close()
    return Image_Type, Size_in_bytes, Sector_size


# Look for the sector where partitions start and partition's description
def run_mmls():
    part_start = []
    part_desc = []
    cmd = mmls + raw_img
    cmd += " > "
    cmd += report_mmls
    # print (cmd)
    os.system(cmd)
    f = open(report_mmls, "r")
    count = 0
    for i in f:
        tmp = i
        if count > 5:
            splited_tmp = tmp[16:len(tmp) - 1].split("   ")
            part_start.append(splited_tmp[0])
            part_desc.append(splited_tmp[len(splited_tmp) - 1])
        count += 1
    f.close()
    return part_start, part_desc


# List all objects in every partitions and load it to database
def run_fls(con, sobj_id, pobj_id, part_start):
    f = open(object_obj_id, "r")
    oobj_id = f.read()
    oobj_id_int = int(oobj_id)
    f.close()

    cmd = fls + "-r -l -o {} ".format(part_start)
    cmd += raw_img
    cmd += " > "
    cmd += report_fls
    # print (cmd)
    os.system(cmd)
    if os.stat(report_fls).st_size == 0:
        return
    f = open(report_fls, "r")
    for i in f:
        fls_data = []
        contents = i
        if 'V/V' in contents or 'v/v' in contents:
            continue
        splited_contents = contents.split("\t")
        tmp = splited_contents[0].split()
        if '+' in tmp[0]:
            fls_data.append(len(tmp[0]))
            fls_data.append(tmp[1])
            if tmp[2] == '*':
                fls_data.append(tmp[2])
            else:
                fls_data.append(None)
        else:
            fls_data.append(0)
            fls_data.append(tmp[0])
            if tmp[1] == '*':
                fls_data.append(tmp[1])
            else:
                fls_data.append(None)
        fls_data.append(tmp[len(tmp) - 1])
        fls_data.append(splited_contents[1])
        fls_data.append(splited_contents[2])
        fls_data.append(splited_contents[3])
        fls_data.append(splited_contents[4])
        fls_data.append(splited_contents[5])
        fls_data.append(splited_contents[6])
        fls_data.append(splited_contents[7])
        fls_data.append(splited_contents[8].strip())

        if "(realloc)" not in fls_data[3]:
            cmd_databases.insert_object(con, oobj_id, sobj_id, pobj_id, fls_data[0], fls_data[1], fls_data[2],
                                        fls_data[3][:-1], fls_data[4], fls_data[5], fls_data[6], fls_data[7],
                                        fls_data[8], fls_data[9], fls_data[10], fls_data[11])
        else:
            cmd_databases.insert_object(con, oobj_id, sobj_id, pobj_id, fls_data[0], fls_data[1], fls_data[2],
                                        fls_data[3][:-10], fls_data[4], fls_data[5], fls_data[6], fls_data[7],
                                        fls_data[8], fls_data[9], fls_data[10], fls_data[11])

        oobj_id_int += 1
        oobj_id = str(oobj_id_int)

    f.close()

    f = open(object_obj_id, "w")
    f.write(oobj_id)
    f.close()


# get sdk version, call log and sms log (android 7 only)
def get_SdkVersion_calllog_SMS():
    sobj_id, xml, calllog, sms = cmd_databases.get_packagesxml_calllogdb_bugledb()
    path = "..\\tmp"
    cmd = icat + "-r -o {} {} {} > {}\\{}".format(xml[1], sobj_id[2], xml[2], path,
                                                      xml[3])  # sobj_id[2] is raw_img
    os.system(cmd)
    cmd_databases.update_SdkVersion(analyze_43.get_SdkVersion(path+"\\packages.xml"))

    if cmd_databases.get_SdkVersion() == 24:
        cmd = icat + "-r -o {} {} {} > {}\\{}".format(calllog[1], sobj_id[2], calllog[2], path,
                                                          calllog[3])  # sobj_id[2] is raw_img
        os.system(cmd)
        cmd = icat + "-r -o {} {} {} > {}\\{}".format(sms[1], sobj_id[2], sms[2], path,
                                                          sms[3])  # sobj_id[2] is raw_img
        os.system(cmd)
        cmd_databases.insert_call_history(analyze_43.get_call_history(path+"\\calllog.db"))
        cmd_databases.insert_sms_history(analyze_43.get_sms_history(path+"\\bugle_db"))


# recovery .apk files
def run_icat(sobj_id, apks):
    path = str(sobj_id[1])
    tpath = path.replace("/", "-")
    tpath = tpath.replace(':', '-')
    tpath = tpath.replace(' ', '-')
    t1path = "C:\\xampp\\htdocs\\api\\result\\" + tpath
    t1path += "\\"
    t1path += "extracted_apks"
    try:
        os.mkdir(t1path)
    except:
        pass
    for apk in apks:
        print(apk)
        cmd = icat + "-r -o {} {} {} > {}\\{}".format(apk[1], sobj_id[2], apk[2], t1path,
                                                      apk[3])  # sobj_id[2] is raw_img
        # print (cmd)
        os.system(cmd)
    return


# run jadx decompiler, search for email, url and ip
def run_jadx(sobj_id):


    def terminate(process):
        if process.poll() is None:
            call('taskkill /F /T /PID ' + str(process.pid))


    apk_package_name = cmd_databases.get_apk_package_name()
    path = str(sobj_id[1])
    tpath = path.replace("/", "-")
    tpath = tpath.replace(':', '-')
    tpath = tpath.replace(' ', '-')
    t1path = "C:\\xampp\\htdocs\\api\\result\\" + tpath
    t1path += "\\"
    t1path += "extracted_apks"
    with os.scandir(t1path) as entries:
        for entry in entries:
            if entry.is_file():
                print(entry.path)
                try:
                    cmd = [jadx, '--escape-unicode', '-d', entry.path[:-4], entry.path,'1>NUL']
                    process = Popen(cmd, stdout=PIPE, stderr=STDOUT, bufsize=1, universal_newlines=True)
                    timer = Timer(5*60, terminate, args=[process])
                    timer.start()
                    for line in iter(process.stdout.readline, ''):
                        print(line, end='')
                    process.stdout.close()
                    process.wait() # wait for the child process to finish
                    timer.cancel()
                except:
                    continue
                for i in apk_package_name:
                    if i[1] == entry.name:
                        cmd_databases.insert_email(analyze_43.find_email(entry.path[:-4], i[2]), i[0])
                        cmd_databases.insert_url(analyze_43.find_url(entry.path[:-4], i[2]), i[0])
                        cmd_databases.insert_ip(analyze_43.find_ip(entry.path[:-4], i[2]), i[0])
                        break
    return


# recovery directories
def run_tsk_recover(sobj_id):
    package_name_attributes = cmd_databases.get_package_name()
    # v = cmd_databases.get_SdkVersion()
    path = str(sobj_id[1])
    tpath = path.replace("/", "-")
    tpath = tpath.replace(':', '-')
    tpath = tpath.replace(' ', '-')

    for package_attribute in package_name_attributes:
        t1path = "C:\\xampp\\htdocs\\api\\result\\" + tpath
        t1path += "\\"
        print (package_attribute[3])
        t1path += package_attribute[3]  # package_attribute[3] means package name
        try:
            os.mkdir(t1path)
        except:
            pass
        cmd = tsk_recover + "-e -o {} -d {} {} {}".format(package_attribute[1], package_attribute[2],
                                                          sobj_id[2], t1path)

        # print (cmd)
        os.system(cmd)

        ext_dirs = cmd_databases.get_external_storage_file(package_attribute[3])
        if ext_dirs:
            for ext_dir in ext_dirs:
                cmd = tsk_recover + "-e -o {} -d {} {} {}".format(ext_dir[1], ext_dir[2],
                                                                  sobj_id[2], t1path)
                os.system(cmd)

        for i in analyze_43.scantree(t1path):
            print(i)
            cmd_databases.insert_file_link(sobj_id[0], package_attribute[3], i[20:], i.split('\\')[-1])


# In each of partitions, run fls tools. By the way, add the image info and partitions info to database
def load_on_db():
    now = datetime.now()
    current_times = now.strftime("%d/%m/%Y %H:%M")
    Image_Type, Size_in_bytes, Sector_size = run_img_stat()

    f = open(source_obj_id, "r")
    sobj_id = f.read()
    sobj_id_int = int(sobj_id)
    f.close()

    con = cmd_databases.create_con()
    cmd_databases.insert_data_source(con, sobj_id, current_times, Image_Type, Size_in_bytes, Sector_size, raw_img)

    part_start, part_desc = run_mmls()

    f = open(part_obj_id, "r")
    pobj_id = f.read()
    pobj_id_int = int(pobj_id)
    f.close()

    # repeat over the partitions
    for i in range(len(part_start)):
        cmd_databases.insert_part(con, pobj_id, sobj_id, part_start[i], part_desc[i])
        run_fls(con, sobj_id, pobj_id, part_start[i])
        pobj_id_int += 1
        pobj_id = str(pobj_id_int)

    cmd_databases.destroy_con(con)

    f = open(part_obj_id, "w")
    f.write(pobj_id)
    f.close()

    sobj_id_int += 1
    sobj_id = str(sobj_id_int)
    f = open(source_obj_id, "w")
    f.write(sobj_id)
    f.close()


def main():
    # """
    begin = time.time()
    print ("checking tools")
    check_raw_img_exist()
    check_tmp_exist()
    check_tools_exist()
    load_on_db()
    # extract SdkVersion
    print ('get Sdk SdkVersion, SMS, contact')
    get_SdkVersion_calllog_SMS()
    # get apks from latest doing
    print ("collect .apk file")
    sobj_id, apks = cmd_databases.get_apks()
    print(sobj_id, apks)
    # create directory base on datetime, will be the report's name
    path = str(sobj_id[1])
    tpath = path.replace("/", "-")
    tpath = tpath.replace(':', '-')
    tpath = tpath.replace(' ', '-')
    t1path = "C:\\xampp\\htdocs\\api\\result\\" + tpath
    try:
        os.mkdir(t1path)
    except:
        pass

    print ("restore .apk files")
    run_icat(sobj_id, apks)
    print ("load info on database")
    android_analysis_17.load_on_db(t1path, apks)
    print ("extract apk files")
    run_jadx(sobj_id)
    print ("recover ralated files")
    run_tsk_recover(sobj_id)

    end = time.time()
    # point out total analysing time
    total_times = "{:0>8}".format(str(timedelta(seconds=round(end - begin))))
    cmd_databases.update_total_times(total_times)
    print(total_times)
    # """


if __name__ == "__main__":
    main()
