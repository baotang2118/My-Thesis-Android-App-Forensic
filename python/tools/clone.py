import multiprocessing
import os
import sys
import subprocess
import time
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("--name", help='name of the image')
args = parser.parse_args()
print (args.name)


# check exist of adb, check root, install busybox, run remote shell and clone device (sdb, sda means backup)
def run_remote_shell():
	result = subprocess.run(['adb', 'shell', 'ls /'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	if result.returncode == 0:
		if "permission denied" in str(result.stdout):
			print ("no root permission")
			return
	else:
		if result.stderr:
			print (result.stderr)

	result = subprocess.run(['adb', 'install', 'BusyBox.apk'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	if result.returncode == 0:
		print (result.stdout)
	else:
		if result.stderr:
			print (result.stderr)

	result = subprocess.run(['adb', 'shell', 'cat /proc/partitions'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	if result.returncode == 0:
		print (result.stdout)
	else:
		if result.stderr:
			print (result.stderr)

	result = subprocess.run(['adb', 'shell', 'dd if=/dev/block/sdb | busybox nc -l -p 8888'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	if result.returncode == 0:
		print (result.stdout)
	else:
		if result.stderr:
			print (result.stderr)


# check exist of adb, start local shell, run ncat and uninstall busybox
def run_local_shell():
	result = subprocess.run(['adb', 'shell', 'ls /'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	if result.returncode == 0:
		if "permission denied" in str(result.stdout):
			print ("no root permission")
			return
	else:
		if result.stderr:
			print (result.stderr)

	time.sleep(5)
	result = subprocess.run(['adb', 'forward', 'tcp:8888', 'tcp:8888'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	if result.returncode == 0:
		print (result.stdout)
	else:
		if result.stderr:
			print (result.stderr)

	os.system('ncat.exe 127.0.0.1 8888 > {}'.format(args.name))

	result = subprocess.run(['adb', 'uninstall', 'stericson.busybox'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	if result.returncode == 0:
		print (result.stdout)
	else:
		if result.stderr:
			print (result.stderr)


if __name__ == "__main__":
    # creating processes
    p1 = multiprocessing.Process(target=run_remote_shell)
    p2 = multiprocessing.Process(target=run_local_shell)

    # starting process 1
    p1.start()
    # starting process 2
    p2.start()

    # wait until process 1 is finished
    p1.join()
    # wait until process 2 is finished
    p2.join()

    # both processes finished
    print("Done!")
