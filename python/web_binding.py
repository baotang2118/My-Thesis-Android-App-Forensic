import mysql.connector
import time
import os
import sys


def CreateDB():
	mydb = mysql.connector.connect(
		host="localhost",
		user="root",
		passwd=""
		)

	mycursor = mydb.cursor()
	mycursor.execute("CREATE DATABASE IF NOT EXISTS thesis_1920_waiting_queue")
	mycursor.close()
	mydb.close()
	return

def CreateTable():
	mydb = mysql.connector.connect(
		host="localhost",
		user="root",
		passwd="",
		database="thesis_1920_waiting_queue"
		)

	mycursor = mydb.cursor()

	mycursor.execute("CREATE TABLE IF NOT EXISTS queue (id INT AUTO_INCREMENT PRIMARY KEY,"
				"cmd TEXT NOT NULL,"
				"source TEXT NOT NULL,"
				"status TEXT);")

	mycursor.close()
	mydb.close()


# # get job
def get_cmd():
	mydb = mysql.connector.connect(
		host="localhost",
		user="root",
		passwd="",
		database="thesis_1920_waiting_queue"
	)
	print (mydb)
	mycursor = mydb.cursor()
	print (mycursor)
	mycursor.execute("SELECT id, cmd, source FROM queue WHERE status is NULL LIMIT 1")
	cmd = mycursor.fetchone()
	mycursor.close()
	mydb.close()	
	return cmd


# update job status
def update_job_status(id):
	mydb = mysql.connector.connect(
		host="localhost",
		user="root",
		passwd="",
		database="thesis_1920_waiting_queue"
	)
	mycursor = mydb.cursor()
	mycursor.execute("UPDATE queue SET status = 'Done' WHERE id = %s", (id,))
	mydb.commit()
	mycursor.close()
	mydb.close()


def main():
	CreateDB()
	CreateTable()
	print ("web binding is running ...")
	print ("It will check databases every 30s or done job")
	print ("Press Ctrl+C to stop")

	try:
		while (1):
			out = get_cmd()
			print (out)
			try:
				print ("Doing task {}".format(out[0]))
				print (out[2])
				os.system(out[1])
			except:
				time.sleep(5)
				continue
			update_job_status(out[0])
			time.sleep(2)
	except KeyboardInterrupt:
		
		print ("Process is terminated")
		sys.exit(0)


if __name__ == "__main__":
    main()