import mysql.connector
import json
from sqlite3 import Error
import random

# basic functions
def create_con():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="thesis_1920_result"
        )
    return mydb


def destroy_con(mydb):
    mydb.close()


def create_need():
    # create database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd=""
        )

    mycursor = mydb.cursor()
    mycursor.execute("CREATE DATABASE IF NOT EXISTS thesis_1920_result")
    mycursor.close()
    mydb.close()

    # create table
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="thesis_1920_result"
        )

    mycursor = mydb.cursor()

    mycursor.execute(
        "CREATE TABLE IF NOT EXISTS data_source (obj_id INT PRIMARY KEY, current_times text, total_times text, type text, size_in_bytes text, section text, path_to_source text, SdkVersion INT)")
    mycursor.execute(
        "CREATE TABLE IF NOT EXISTS part (obj_id INT PRIMARY KEY, source INT, start VARCHAR(100), describe0 VARCHAR(100), FOREIGN KEY(source) REFERENCES data_source(obj_id))")
    mycursor.execute('''CREATE TABLE IF NOT EXISTS object (obj_id INT PRIMARY KEY, source INT, part INT, dlevel INT, ftype text, deleted text, metadata_addr text, name text, 
                                                    mtime text, atime text, ctime text, crtime text, size text, uid text, gid text, FOREIGN KEY(source) REFERENCES data_source(obj_id), 
                                                    FOREIGN KEY(part) REFERENCES part(obj_id))''')
    mycursor.execute(
        "CREATE TABLE IF NOT EXISTS apk_files_info (apk_id INT PRIMARY KEY, appName NVARCHAR(260), packageName VARCHAR(260), androidversionCode text, androidversionName text, path2Icon text, cert NVARCHAR(3000), FOREIGN KEY(apk_id) REFERENCES object(obj_id))")
    mycursor.execute(
        "CREATE TABLE IF NOT EXISTS apk_files_detail (apk_id INT PRIMARY KEY, MD5 VARCHAR(35), SHA1 VARCHAR(40), SHA256 VARCHAR(64), sendBroadcast INT, onReceive INT, startService INT, onHandleIntent INT, startActivity INT, getIntent INT, FOREIGN KEY(apk_id) REFERENCES object(obj_id))")
    mycursor.execute(
        "CREATE TABLE IF NOT EXISTS apk_files_detail_components (apk_id INT, ComponentName VARCHAR(300), ComponentType VARCHAR(20), ExportStatus VARCHAR(10), PRIMARY KEY (apk_id, ComponentName), FOREIGN KEY(apk_id) REFERENCES object(obj_id))")
    mycursor.execute(
        "CREATE TABLE IF NOT EXISTS apk_files_detail_permissions (apk_id INT, PermissionName VARCHAR(300), PRIMARY KEY (apk_id, PermissionName), FOREIGN KEY(apk_id) REFERENCES object(obj_id))")
    mycursor.execute(
        "CREATE TABLE IF NOT EXISTS apk_files_email (apk_id INT, email VARCHAR(320), PRIMARY KEY (apk_id, email), FOREIGN KEY(apk_id) REFERENCES object(obj_id))")
    mycursor.execute(
        "CREATE TABLE IF NOT EXISTS apk_files_url (apk_id INT, url VARCHAR(320), PRIMARY KEY (apk_id, url), FOREIGN KEY(apk_id) REFERENCES object(obj_id))")
    mycursor.execute(
        "CREATE TABLE IF NOT EXISTS apk_files_ip (apk_id INT, ip VARCHAR(100), PRIMARY KEY (apk_id, ip), FOREIGN KEY(apk_id) REFERENCES object(obj_id))")
    mycursor.execute(
        "CREATE TABLE IF NOT EXISTS recovered_file (id INT PRIMARY KEY AUTO_INCREMENT, reportID INT, package_name VARCHAR(260), link_to_file text, file_name VARCHAR(260), FOREIGN KEY(reportID) REFERENCES data_source(obj_id))")
    mycursor.execute(
        "CREATE TABLE IF NOT EXISTS call_history (id INT PRIMARY KEY AUTO_INCREMENT, reportID INT, _id INT, number VARCHAR(30), date BIGINT, duration INT, type INT, geocoded_location TEXT, FOREIGN KEY(reportID) REFERENCES data_source(obj_id))")
    mycursor.execute(
        "CREATE TABLE IF NOT EXISTS sms_history_conversation_participants (id INT PRIMARY KEY AUTO_INCREMENT, reportID INT, _id INT, conversation_id INT, participant_id INT, FOREIGN KEY(reportID) REFERENCES data_source(obj_id))")
    mycursor.execute(
        "CREATE TABLE IF NOT EXISTS sms_history_conversations (id INT PRIMARY KEY AUTO_INCREMENT, reportID INT, _id INT, sms_thread_id INT, name TEXT, latest_message_id INT, snippet_text TEXT, subject_text TEXT, preview_uri TEXT, preview_content_type TEXT, show_draft INT, draft_snippet_text TEXT, draft_subject_text TEXT, draft_preview_uri TEXT, draft_preview_content_type TEXT, archive_status INT, sort_timestamp BIGINT, last_read_timestamp BIGINT, icon TEXT, participant_contact_id INT, participant_lookup_key TEXT, participant_normalized_destination TEXT, current_self_id TEXT, participant_count INT, notification_enabled INT, notification_sound_uri TEXT, notification_vibration INT, include_email_addr INT, sms_service_center TEXT, FOREIGN KEY(reportID) REFERENCES data_source(obj_id))")
    mycursor.execute(
        "CREATE TABLE IF NOT EXISTS sms_history_messages (id INT PRIMARY KEY AUTO_INCREMENT, reportID INT, _id INT, conversation_id INT, sender_id INT, sent_timestamp BIGINT, received_timestamp BIGINT, message_protocol INT, message_status INT, seen INT, read0 INT, sms_message_uri TEXT, sms_priority INT, sms_message_size INT, mms_subject TEXT, mms_transaction_id TEXT, mms_content_location TEXT, mms_expiry BIGINT, raw_status INT, self_id INT, retry_start_timestamp BIGINT, FOREIGN KEY(reportID) REFERENCES data_source(obj_id))")
    mycursor.execute(
        "CREATE TABLE IF NOT EXISTS sms_history_participants (id INT PRIMARY KEY AUTO_INCREMENT, reportID INT, _id INT, sub_id INT, sim_slot_id INT, normalized_destination TEXT, send_destination TEXT, display_destination TEXT, full_name TEXT,first_name TEXT, profile_photo_uri TEXT, contact_id INT, lookup_key TEXT, blocked INT, subscription_name TEXT, subscription_color INT, contact_destination TEXT, FOREIGN KEY(reportID) REFERENCES data_source(obj_id))")
    mycursor.execute(
        "CREATE TABLE IF NOT EXISTS sms_history_parts (id INT PRIMARY KEY AUTO_INCREMENT, reportID INT, _id INT, message_id INT, text TEXT, uri TEXT, content_type TEXT, width INT, height INT,timestamp BIGINT, conversation_id INT, FOREIGN KEY(reportID) REFERENCES data_source(obj_id))")

    # create table Dangerous Permission
    mycursor.execute(
        "CREATE TABLE IF NOT EXISTS dangerous_permission (PermissionGroup VARCHAR(15), PermissionName VARCHAR(30), PRIMARY KEY (PermissionGroup,PermissionName))")
    sql = "INSERT IGNORE INTO dangerous_permission (PermissionGroup, PermissionName) VALUES (%s, %s)"
    val = ("CALENDAR", "READ_CALENDAR")
    mycursor.execute(sql, val)
    val = ("CALENDAR", "WRITE_CALENDAR")
    mycursor.execute(sql, val)

    val = ("CALL_LOG", "READ_CALL_LOG")
    mycursor.execute(sql, val)
    val = ("CALL_LOG", "WRITE_CALL_LOG")
    mycursor.execute(sql, val)
    val = ("CALL_LOG", "PROCESS_OUTGOING_CALLS")
    mycursor.execute(sql, val)

    val = ("CAMERA", "CAMERA")
    mycursor.execute(sql, val)

    val = ("CONTACTS", "READ_CONTACTS")
    mycursor.execute(sql, val)
    val = ("CONTACTS", "WRITE_CONTACTS")
    mycursor.execute(sql, val)
    val = ("CONTACTS", "GET_ACCOUNTS")
    mycursor.execute(sql, val)

    val = ("LOCATION", "ACCESS_FINE_LOCATION")
    mycursor.execute(sql, val)
    val = ("LOCATION", "ACCESS_COARSE_LOCATION")
    mycursor.execute(sql, val)

    val = ("MICROPHONE", "RECORD_AUDIO")
    mycursor.execute(sql, val)

    val = ("PHONE", "READ_PHONE_STATE")
    mycursor.execute(sql, val)
    val = ("PHONE", "READ_PHONE_NUMBERS")
    mycursor.execute(sql, val)
    val = ("PHONE", "CALL_PHONE")
    mycursor.execute(sql, val)
    val = ("PHONE", "ANSWER_PHONE_CALLS")
    mycursor.execute(sql, val)
    val = ("PHONE", "ADD_VOICEMAIL")
    mycursor.execute(sql, val)
    val = ("PHONE", "USE_SIP")
    mycursor.execute(sql, val)

    val = ("SENSORS", "BODY_SENSORS")
    mycursor.execute(sql, val)

    val = ("SMS", "SEND_SMS")
    mycursor.execute(sql, val)
    val = ("SMS", "RECEIVE_SMS")
    mycursor.execute(sql, val)
    val = ("SMS", "READ_SMS")
    mycursor.execute(sql, val)
    val = ("SMS", "RECEIVE_WAP_PUSH")
    mycursor.execute(sql, val)
    val = ("SMS", "RECEIVE_MMS")
    mycursor.execute(sql, val)

    val = ("STORAGE", "READ_EXTERNAL_STORAGE")
    mycursor.execute(sql, val)
    val = ("STORAGE", "WRITE_EXTERNAL_STORAGE")
    mycursor.execute(sql, val)
    mydb.commit()

    mycursor.close()
    mydb.close()


def insert_data_source(mydb, obj_id, current_times, img_type, size_in_bytes, section, path_to_source):
    mycursor = mydb.cursor()
    mycursor.execute(
        'INSERT INTO data_source(obj_id, current_times, type, size_in_bytes, section, path_to_source) VALUES( %s, %s, %s, %s, %s, %s)',
        (obj_id, current_times, img_type, size_in_bytes, section, path_to_source))
    mydb.commit()
    mycursor.close()


def insert_part(mydb, obj_id, source, start, describe0):
    mycursor = mydb.cursor()
    mycursor .execute('INSERT INTO part(obj_id, source, start, describe0) VALUES(%s, %s, %s, %s)',
              (obj_id, source, start, describe0))
    mydb.commit()
    mycursor.close()


def insert_object(mydb, obj_id, source, part, dlevel, ftype, deleted, metadata_addr, name, mtime, atime, ctime, crtime,
                  size, uid, gid):
    mycursor = mydb.cursor()
    mycursor.execute(
        'INSERT INTO object(obj_id, source, part, dlevel, ftype, deleted, metadata_addr, name, mtime, atime, ctime, crtime, size, uid, gid) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
        (obj_id, source, part, dlevel, ftype, deleted, metadata_addr, name, mtime, atime, ctime, crtime, size, uid,
         gid))
    mydb.commit()
    mycursor.close()


# get packages.xml, call logs and sms log
def get_packagesxml_calllogdb_bugledb():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="thesis_1920_result"
        )

    mycursor = mydb.cursor()

    mycursor.execute("SELECT obj_id, current_times, path_to_source FROM data_source ORDER BY obj_id DESC LIMIT 1")
    sobj_id = mycursor.fetchone()
    mycursor.execute(
        "SELECT object.obj_id, part.start, object.metadata_addr, object.name FROM object INNER JOIN part on part.obj_id = object.part WHERE object.name = 'packages.xml' AND object.source = %s",
        (sobj_id[0],))
    packagesxml = mycursor.fetchone()
    mycursor.execute(
        "SELECT object.obj_id, part.start, object.metadata_addr, object.name FROM object INNER JOIN part on part.obj_id = object.part WHERE object.name = 'calllog.db' AND object.source = %s",
        (sobj_id[0],))
    calllog = mycursor.fetchone()
    mycursor.execute(
        "SELECT object.obj_id, part.start, object.metadata_addr, object.name FROM object INNER JOIN part on part.obj_id = object.part WHERE object.name = 'bugle_db' AND object.source = %s",
        (sobj_id[0],))
    bugle = mycursor.fetchone()
    mycursor.close()
    mydb.close()
    return sobj_id, packagesxml, calllog, bugle


# get list of .apk files depends on android version
def get_apks():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="thesis_1920_result"
        )

    mycursor = mydb.cursor()

    mycursor.execute("SELECT obj_id, current_times, path_to_source FROM data_source ORDER BY obj_id DESC LIMIT 1")
    sobj_id = mycursor.fetchone()
    mycursor.execute(
        "SELECT object.obj_id, part.start, object.metadata_addr, object.name FROM object INNER JOIN part on part.obj_id = object.part WHERE object.name LIKE '%.apk' AND object.source = %s",
        (sobj_id[0],))
    apks = mycursor.fetchall()
    mycursor.close()
    mydb.close()
    if get_SdkVersion() > 20:
        tmp = []
        for i in apks:
            listi = list(i)
            while (1):
                tmp1 = listi[3].split('.')
                tmp1[0] += str(random.randint(0,1000))
                tmp1[0] += '.'
                listi[3] = tmp1[0] + tmp1[1]
                if listi not in tmp:
                    break
            tuplei = tuple(listi)
            tmp.append(tuplei)
        return sobj_id, tmp
    else:
        return sobj_id, apks


# get list of .apk attribute such as object id, beginning of partitions, address, name
def get_package_name():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="thesis_1920_result"
        )

    mycursor = mydb.cursor()

    mycursor.execute("SELECT obj_id FROM data_source ORDER BY obj_id DESC LIMIT 1")
    sobj_id = mycursor.fetchone()
    mycursor.execute(
        "SELECT object.obj_id, part.start, object.metadata_addr, object.name FROM object INNER JOIN part on part.obj_id = object.part WHERE object.source = %s AND object.name IN ( SELECT apk_files_info.packageName FROM object INNER JOIN apk_files_info on object.obj_id = apk_files_info.apk_id WHERE object.source = %s)",
        (sobj_id[0], sobj_id[0],))
    package_name = mycursor.fetchall()
    
    if get_SdkVersion() > 20 and get_SdkVersion() < 26:
        mycursor.execute(
            "SELECT object.obj_id, part.start, object.metadata_addr, object.name FROM object INNER JOIN part on part.obj_id = object.part WHERE object.source = %s AND object.name IN ( SELECT CONCAT(apk_files_info.packageName,'-1') FROM object INNER JOIN apk_files_info on object.obj_id = apk_files_info.apk_id WHERE object.source = %s)",
            (sobj_id[0], sobj_id[0],))
        package_name1 = mycursor.fetchall()
        for i in package_name1:
            package_name.append(i)
    
    if get_SdkVersion() >= 26:
        mycursor.execute(
            "SELECT CONCAT(apk_files_info.packageName,'-') FROM object INNER JOIN apk_files_info on object.obj_id = apk_files_info.apk_id WHERE object.source = %s",
            (sobj_id[0],))
        package_name1 = mycursor.fetchall()
        for i in package_name1:
            mycursor.execute(
                "SELECT object.obj_id, part.start, object.metadata_addr, object.name FROM object INNER JOIN part on part.obj_id = object.part WHERE object.source = %s AND object.name LIKE %s",
                (sobj_id[0], i[0]+'%',))
            package_name2 = mycursor.fetchall()
            for j in package_name2:
                package_name.append(j)
    
    mycursor.close()
    mydb.close()

    return package_name


def get_apk_package_name():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="thesis_1920_result"
        )

    mycursor = mydb.cursor()

    mycursor.execute("SELECT obj_id FROM data_source ORDER BY obj_id DESC LIMIT 1")
    sobj_id = mycursor.fetchone()
    mycursor.execute(
        "SELECT object.obj_id, object.name, apk_files_info.packageName FROM object INNER JOIN apk_files_info on object.obj_id = apk_files_info.apk_id WHERE object.source = %s",
        (sobj_id[0],))
    apk_package_name = mycursor.fetchall()
    mycursor.close()
    mydb.close()
    return apk_package_name


# update total analysing time
def update_total_times(total_times):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="thesis_1920_result"
        )

    mycursor = mydb.cursor()
    
    mycursor.execute(
        "UPDATE data_source SET total_times = %s WHERE obj_id = (SELECT obj_id FROM data_source ORDER BY obj_id DESC LIMIT 1)",
        (total_times,))
    mydb.commit()
    mycursor.close()
    mydb.close()


# update Android version
def update_SdkVersion(v):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="thesis_1920_result"
        )

    mycursor = mydb.cursor()
    
    mycursor.execute(
        "UPDATE data_source SET SdkVersion = %s WHERE obj_id = (SELECT obj_id FROM data_source ORDER BY obj_id DESC LIMIT 1)",
        (v,))
    mydb.commit()
    mycursor.close()
    mydb.close()


# Insert call history (android 7 only)
def insert_call_history(history):
    if not history:
        return
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="thesis_1920_result"
        )
    mycursor = mydb.cursor()
    
    mycursor.execute("SELECT obj_id FROM data_source ORDER BY obj_id DESC LIMIT 1")
    sobj_id = mycursor.fetchone()

    sql = "INSERT INTO call_history(reportID, _id, number, date, duration, type, geocoded_location) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    for i in range(0, len(history)):
        mycursor.execute(sql, (sobj_id[0], history[i][0], history[i][1], history[i][2], history[i][3], history[i][4], history[i][5]))
    
    mydb.commit()
    mycursor.close()
    mydb.close()

# Insert sms history (android 7 only)
def insert_sms_history(sms):
    if not sms:
        return
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="thesis_1920_result"
        )
    mycursor = mydb.cursor()
    
    mycursor.execute("SELECT obj_id FROM data_source ORDER BY obj_id DESC LIMIT 1")
    sobj_id = mycursor.fetchone()

    result1 = sms[0]
    result2 = sms[1]
    result3 = sms[2]
    result4 = sms[3]
    result5 = sms[4]

    sql = "INSERT INTO sms_history_conversation_participants(reportID, _id, conversation_id, participant_id) VALUES (%s, %s, %s, %s)"
    for i in range(0, len(result1)):
        mycursor.execute(sql, (sobj_id[0], result1[i][0], result1[i][1], result1[i][2]))

    sql = '''INSERT INTO sms_history_conversations(reportID, _id, sms_thread_id, name, latest_message_id, snippet_text, subject_text, preview_uri, 
                                                    preview_content_type, show_draft, draft_snippet_text, draft_subject_text, draft_preview_uri, draft_preview_content_type, archive_status, 
                                                    sort_timestamp, last_read_timestamp, icon, participant_contact_id, participant_lookup_key, participant_normalized_destination, current_self_id, 
                                                    participant_count, notification_enabled, notification_sound_uri, notification_vibration, include_email_addr, sms_service_center) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 
                            %s, %s, %s, %s, %s, %s, %s, 
                            %s, %s, %s, %s, %s, %s, %s, 
                            %s, %s, %s, %s, %s, %s)'''
    for i in range(0, len(result2)):
        mycursor.execute(sql, (sobj_id[0], result2[i][0], result2[i][1], result2[i][2], result2[i][3], result2[i][4], result2[i][5],
                        result2[i][6], result2[i][7], result2[i][8], result2[i][9], result2[i][10], result2[i][11], result2[i][12], result2[i][13], result2[i][14],
                        result2[i][15], result2[i][16], result2[i][17], result2[i][18], result2[i][19], result2[i][20], result2[i][21], result2[i][22], result2[i][23],
                        result2[i][24], result2[i][25], result2[i][26]))

    sql = '''INSERT INTO sms_history_messages(reportID, _id, conversation_id, sender_id, sent_timestamp, received_timestamp, message_protocol, 
            message_status, seen, read0, sms_message_uri, sms_priority, sms_message_size, mms_subject, mms_transaction_id, mms_content_location, 
            mms_expiry, raw_status, self_id, retry_start_timestamp) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
    for i in range(0, len(result3)):
        mycursor.execute(sql, (sobj_id[0], result3[i][0], result3[i][1], result3[i][2], result3[i][3], result3[i][4], result3[i][5],
                        result3[i][6], result3[i][7], result3[i][8], result3[i][9], result3[i][10], result3[i][11], result3[i][12], result3[i][13], result3[i][14],
                        result3[i][15], result3[i][16], result3[i][17], result3[i][18]))

    sql = '''INSERT INTO sms_history_participants(reportID, _id, sub_id, sim_slot_id, normalized_destination, send_destination, display_destination, 
    full_name,first_name, profile_photo_uri, contact_id, lookup_key, blocked, subscription_name, subscription_color, contact_destination) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
    for i in range(0, len(result4)):
        mycursor.execute(sql, (sobj_id[0], result4[i][0], result4[i][1], result4[i][2], result4[i][3], result4[i][4], result4[i][5], 
            result4[i][6], result4[i][7], result4[i][8], result4[i][9], result4[i][10], result4[i][11], result4[i][12], result4[i][13], result4[i][14]))

    sql = '''INSERT INTO sms_history_parts(reportID, _id, message_id, text, uri, content_type, width, height,timestamp, conversation_id) VALUES (%s, %s, %s,%s, %s,%s, %s,%s, %s,%s)'''
    for i in range(0, len(result5)):
        mycursor.execute(sql, (sobj_id[0], result5[i][0], result5[i][1], result5[i][2], result5[i][3], result5[i][4], result5[i][5], result5[i][6], result5[i][7], result5[i][8]))
    mydb.commit()
    mycursor.close()
    mydb.close()


def get_SdkVersion():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="thesis_1920_result"
        )

    mycursor = mydb.cursor()
    
    mycursor.execute(
        "SELECT SdkVersion FROM data_source WHERE obj_id = (SELECT obj_id FROM data_source ORDER BY obj_id DESC LIMIT 1)")
    v = mycursor.fetchone()
    mycursor.close()
    mydb.close()
    return v[0]


def insert_apk_files_info(apks, apkslist):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="thesis_1920_result"
        )

    mycursor = mydb.cursor()
    
    sql = "INSERT INTO apk_files_info(apk_id, appName, packageName, androidversionCode, androidversionName, path2Icon, cert) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    # app name comes from androguard
    # apk file name apks[i][1]
    # print ("debug thong tin day apk", apks) # ti comment lai
    # print ("debug ds apk", apkslist) # ti comment lai
    for i in range(1, len(apks)):
        if len(apks[i]) < 8: # skip nhung file dump khong co gi
            continue
        for tmp in apkslist:
            if tmp[3] == apks[i][1]:
                apks[i][0] = tmp[0]
                break

        try:
            print (apks[i])
            mycursor.execute(sql, (apks[i][0], apks[i][2], apks[i][3], apks[i][4], apks[i][5], apks[i][6], apks[i][7]))
        except:
            print (apks[i])
            print ("no cert")
            mycursor.execute(sql, (apks[i][0], apks[i][2], apks[i][3], apks[i][4], apks[i][5], apks[i][6], "N/A")) # fix python 3.7.5 bug
    mydb.commit()
    mycursor.close()
    mydb.close()


def insert_apk_files_detail(japks, apkslist):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="thesis_1920_result"
        )

    mycursor = mydb.cursor()
    
    sql = "INSERT INTO apk_files_detail(apk_id, MD5, SHA1, SHA256, sendBroadcast, onReceive, startService, onHandleIntent, startActivity, getIntent) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    sql_com = "INSERT INTO apk_files_detail_components(apk_id, ComponentName, ComponentType, ExportStatus) VALUES (%s, %s, %s, %s)"
    sql_permission = "INSERT INTO apk_files_detail_permissions(apk_id, PermissionName) VALUES ( %s, %s)"
    apks = json.loads(japks)
    detail = apks["tableCountMethod"]
    # input is a list of apks, so we loop through each apk in this list
    for i in range(1, len(detail)):
        if len(detail[i]) < 8:
            continue
        # print (detail[i])
        # detail[i][1] is app name/file name/ apk name (it's not package name nor app name that come from androguard digger)
        # compare app name to map the other object id
        for apk in apkslist:
            if apk[3] == detail[i][1]:
                detail[i][0] = apk[0]
                break
        try:
            # insert into table apk_files_detail
            # detail[i][0] is object id
            # detail[i][2], detail[i][3], detail[i][4] are hash
            # detail[i][5], detail[i][6], detail[i][7], detail[i][8], detail[i][9] and detail[i][10] are sendBroadcast, onReceive, startService,
            #                                                                                           onHandleIntent, startActivity and getIntent, respectively
            if ((detail[i][5] or detail[i][6] or detail[i][7] or detail[i][8] or detail[i][9] or detail[i][
                10]) == "Failed!"):
                mycursor.execute(sql, (detail[i][0], '', '', '', -1, -1, -1, -1, -1, -1))
            else:
                mycursor.execute(sql, (
                detail[i][0], detail[i][2], detail[i][3], detail[i][4], detail[i][5], detail[i][6], detail[i][7],
                detail[i][8], detail[i][9], detail[i][10]))
        except Exception as e:
            print(e)
        # component is a list type, so we repeat over this
        for j in range(0, len(detail[i][12])):
            try:
                # insert into table apk_files_detail_components
                # detail[i][0], detail[i][12][j], detail[i][11][j] and detail[i][13][j] are ComponentName, ComponentType nad ExportStatus, resepctively
                mycursor.execute(sql_com, (detail[i][0], detail[i][12][j], detail[i][11][j], detail[i][13][j]))
            except Exception as e:
                print(e)
        # permission is also a list type
        for j in range(0, len(detail[i][14])):
            try:
                # insert into table apk_files_detail_components
                # detail[i][14][j] are PermissionName
                mycursor.execute(sql_permission, (detail[i][0], detail[i][14][j]))
            except Exception as e:
                print(e)
    mydb.commit()
    mycursor.close()
    mydb.close()


def insert_email(emails, apk_id):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="thesis_1920_result"
        )

    mycursor = mydb.cursor()
    
    sql = "INSERT INTO apk_files_email(apk_id, email) VALUES (%s, %s)"
    for i in emails:
        mycursor.execute(sql, (apk_id, i))
    mydb.commit()
    mycursor.close()
    mydb.close()


def insert_url(urls, apk_id):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="thesis_1920_result"
        )

    mycursor = mydb.cursor()
    
    sql = "INSERT INTO apk_files_url(apk_id, url) VALUES (%s, %s)"
    for i in urls:
        mycursor.execute(sql, (apk_id, i))
    mydb.commit()
    mycursor.close()
    mydb.close()


def insert_ip(ips, apk_id):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="thesis_1920_result"
        )

    mycursor = mydb.cursor()
    
    sql = "INSERT INTO apk_files_ip(apk_id, ip) VALUES (%s, %s)"
    for i in ips:
        mycursor.execute(sql, (apk_id, i))
    mydb.commit()
    mycursor.close()
    mydb.close()


def insert_file_link(reportID, package_name, link_to_file, file_name):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="thesis_1920_result"
        )

    mycursor = mydb.cursor()
    
    sql = "SELECT 1 FROM recovered_file WHERE reportID = %s AND package_name = %s AND link_to_file = %s AND file_name = %s"
    mycursor.execute(sql, (reportID, package_name, link_to_file, file_name,))
    tmp = mycursor.fetchall()
    if not tmp:
        sql = "INSERT INTO recovered_file(reportID, package_name, link_to_file, file_name) VALUES (%s, %s, %s, %s)"
        mycursor.execute(sql, (reportID, package_name, link_to_file, file_name))
    mydb.commit()
    mycursor.close()
    mydb.close()


def get_external_storage_file(package_name):
    ext_dir = None
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="thesis_1920_datasheet_databases"
        )

    mycursor = mydb.cursor()
    
    sql = "SELECT dir FROM datasheet WHERE package_name = %s"
    mycursor.execute(sql, (package_name,))
    tmp = mycursor.fetchall()
    mycursor.close()
    mydb.close()

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="thesis_1920_result"
        )

    mycursor = mydb.cursor()
    
    mycursor.execute("SELECT obj_id FROM data_source ORDER BY obj_id DESC LIMIT 1")
    sobj_id = mycursor.fetchone()
    sql = "SELECT object.obj_id, part.start, object.metadata_addr FROM object INNER JOIN part on part.obj_id = object.part WHERE object.source = %s AND object.name = %s"

    for i in tmp:
        for j in i:
            j = j.split(',')
            for k in j:
                mycursor.execute(sql, (sobj_id[0], k,))
                tmp1 = mycursor.fetchall()
                if tmp1:
                    ext_dir = tmp1
    mycursor.close()
    mydb.close()
    print(ext_dir)
    return ext_dir


def main():
    create_need()
    # get_package_name()


if __name__ == "__main__":
    main()
