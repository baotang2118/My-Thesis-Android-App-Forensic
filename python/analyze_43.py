import re
import os
import sqlite3
from bs4 import BeautifulSoup


# get Sdk version
def get_SdkVersion(packagesxml):
	f = open(packagesxml, "r")
	soup = BeautifulSoup(f, 'xml')
	try:
		v = soup.packages.version.get('sdkVersion')
	except:
		p = soup.packages
		lpv = p.find("last-platform-version")
		v = lpv.get("internal")
	f.close()
	return  int(v)


# get call history from sqlite file (for android 7 only)
def get_call_history(path):
	if os.path.exists(path):
		conn = sqlite3.connect(path)
		c = conn.cursor()
		c.execute("SELECT _id, number, date, duration, type, geocoded_location FROM calls")
		result = c.fetchall()
		conn.close()

		os.remove(path)

		return result
	else:
		return


# get sms history from sqlite file (for android 7 only)
def get_sms_history(path):
	if os.path.exists(path):
		conn = sqlite3.connect(path)
		c = conn.cursor()
		c.execute("SELECT _id, conversation_id, participant_id FROM conversation_participants")
		result1 = c.fetchall()
		c.execute("SELECT _id, sms_thread_id, name, latest_message_id, snippet_text, subject_text, preview_uri, preview_content_type, show_draft, draft_snippet_text, draft_subject_text, draft_preview_uri, draft_preview_content_type, archive_status, sort_timestamp, last_read_timestamp, icon, participant_contact_id, participant_lookup_key, participant_normalized_destination, current_self_id, participant_count, notification_enabled, notification_sound_uri, notification_vibration, include_email_addr, sms_service_center FROM conversations")
		result2 = c.fetchall()
		c.execute("SELECT _id, conversation_id, sender_id, sent_timestamp, received_timestamp, message_protocol, message_status, seen, read, sms_message_uri, sms_priority, sms_message_size, mms_subject, mms_transaction_id, mms_content_location, mms_expiry, raw_status, self_id, retry_start_timestamp FROM messages")
		result3 = c.fetchall()
		c.execute("SELECT _id, sub_id, sim_slot_id, normalized_destination, send_destination, display_destination, full_name,first_name, profile_photo_uri, contact_id, lookup_key, blocked, subscription_name, subscription_color, contact_destination FROM participants")
		result4 = c.fetchall()
		c.execute("SELECT _id, message_id, text, uri, content_type, width, height, timestamp, conversation_id FROM parts")
		result5 = c.fetchall()

		conn.close()

		os.remove(path)

		return result1, result2, result3, result4, result5
	else:
		return

# scan dir tree recursion
def scantree(path_name):
	try:
		for entry in os.scandir(path_name):
			if entry.is_dir(follow_symlinks=False):
				yield from scantree(entry.path)
			else:
				yield entry.path
	except:
		yield


# find email	
def find_email(link_java, package_name, fastmode = True):
	email_list = []
	tmp = package_name.split('.')
	gen = scantree(link_java + "\\sources\\{}\\{}".format(tmp[0], tmp[1]))
	for i in gen:
		if not i:
			continue
		if fastmode:
			if i.endswith('.java') or i.endswith('.xml') or i.endswith('.json'):
				try:
					file = open(i, "r")
					for line in file:
						email = re.findall('[a-zA-Z0-9+_\-\.]+@[0-9a-zA-Z][.-0-9a-zA-Z]*.[a-zA-Z]+', line)
						if email:
							email_list.append(email)
				except:
					continue
		else:
			try:
				file = open(i, "r")
				for line in file:
					email = re.findall('[a-zA-Z0-9+_\-\.]+@[0-9a-zA-Z][.-0-9a-zA-Z]*.[a-zA-Z]+', line)
					if email:
						email_list.append(email)
			except:
				continue
	
	gen = scantree(link_java + "\\resources\\res\\")
	for i in gen:
		if not i:
			continue
		if fastmode:
			if i.endswith('.java') or i.endswith('.xml') or i.endswith('.json'):
				try:
					file = open(i, "r")
					for line in file:
						email = re.findall('[a-zA-Z0-9+_\-\.]+@[0-9a-zA-Z][.-0-9a-zA-Z]*.[a-zA-Z]+', line)
						if email:
							email_list.append(email)
				except:
					continue
		else:
			try:
				file = open(i, "r")
				for line in file:
					email = re.findall('[a-zA-Z0-9+_\-\.]+@[0-9a-zA-Z][.-0-9a-zA-Z]*.[a-zA-Z]+', line)
					if email:
						email_list.append(email)
			except:
				continue
	tmp_email_list = []
	for i in email_list:
		for j in i:
			tmp_email_list.append(j)
	return list(dict.fromkeys(tmp_email_list))


# find url
def find_url(link_java, package_name, fastmode = True):
	url_list = []
	tmp = package_name.split('.')
	gen = scantree(link_java + "\\sources\\{}\\{}".format(tmp[0], tmp[1]))
	for i in gen:
		if not i:
			continue
		if fastmode:
			if i.endswith('.java') or i.endswith('.xml') or i.endswith('.json'):
				try:
					file = open(i, "r")
					for line in file:
						url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', line)
						if url:
							url_list.append(url)
				except:
					continue
		else:
			try:
				file = open(i, "r")
				for line in file:
					url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', line)
					if url:
						url_list.append(url)
			except:
				continue
	
	gen = scantree(link_java + "\\resources\\res\\")
	for i in gen:
		if not i:
			continue
		if fastmode:
			if i.endswith('.java') or i.endswith('.xml') or i.endswith('.json'):
				try:
					file = open(i, "r")
					for line in file:
						url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', line)
						if url:
							url_list.append(url)
				except:
					continue
		else:
			try:
				file = open(i, "r")
				for line in file:
					url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', line)
					if url:
						url_list.append(url)
			except:
				continue
	tmp_url_list = []
	for i in url_list:
		for j in i:
			tmp_url_list.append(j)
	return list(dict.fromkeys(tmp_url_list))


# find ip
def find_ip(link_java, package_name, fastmode = True):
	ip_list = []
	tmp = package_name.split('.')
	gen = scantree(link_java + "\\sources\\{}\\{}".format(tmp[0], tmp[1]))
	for i in gen:
		if not i:
			continue
		if fastmode:
			if i.endswith('.java') or i.endswith('.xml') or i.endswith('.json'):
				try:
					file = open(i, "r")
					for line in file:
						ip = re.findall('(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})', line)
						if ip:
							ip_list.append(ip)
				except:
					continue
		else:
			try:
				file = open(i, "r")
				for line in file:
					ip = re.findall('(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})', line)
					if ip:
						ip_list.append(ip)
			except:
				continue
	
	gen = scantree(link_java + "\\resources\\res\\")
	for i in gen:
		if not i:
			continue
		if fastmode:
			if i.endswith('.java') or i.endswith('.xml') or i.endswith('.json'):
				try:
					file = open(i, "r")
					for line in file:
						ip = re.findall('(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})', line)
						if ip:
							ip_list.append(ip)
				except:
					continue
		else:
			try:
				file = open(i, "r")
				for line in file:
					ip = re.findall('(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})', line)
					if ip:
						ip_list.append(ip)
			except:
				continue
	tmp_ip_list = []
	for i in ip_list:
		for j in i:
			tmp_ip_list.append(j)
	return list(dict.fromkeys(tmp_ip_list))

