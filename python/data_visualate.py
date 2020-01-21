import matplotlib.pyplot as plt
import matplotlib.dates as mdate
import numpy as np
import pandas as pd
import folium
import datetime
import mysql.connector
import multiprocessing
import argparse


# Get argurments
parser = argparse.ArgumentParser(description='Android application forensic - Data visualize')
parser.add_argument('--plot', action='store_true', help='To show call and message frequency')
parser.add_argument('--map', action='store_true', help='To show where the location of phone calls')
parser.add_argument('--showmess', action='store_true', help='To show conversation and timeline')
parser.add_argument('--report', type=str, help='Report id')
args = parser.parse_args()


# get data for frequency plot
def get_data_freq(id):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="thesis_1920_result"
        )
    mycursor = mydb.cursor()

    mycursor.execute("SELECT number, date FROM call_history WHERE type = 1 AND reportID = %s", (id,))
    result = mycursor.fetchall()

    x1 = []
    y1 = []
    for i in result:
        y1.append(i[0])
        x1.append(i[1]/1000) #milisec to sec

    mycursor.execute("SELECT number, date FROM call_history WHERE type = 2 AND reportID = %s", (id,))
    result = mycursor.fetchall()

    x2 = []
    y2 = []
    for i in result:
        y2.append(i[0])
        x2.append(i[1]/1000) #milisec to sec

    mycursor.execute("SELECT normalized_destination, received_timestamp FROM sms_history_messages INNER JOIN sms_history_participants ON sms_history_messages.sender_id = sms_history_participants._id WHERE message_status = 100 AND sms_history_messages.reportID = %s", (id,))
    result = mycursor.fetchall()

    x3 = []
    y3 = []
    for i in result:
        y3.append(i[0])
        x3.append(i[1]/1000) #milisec to sec

    mycursor.execute("SELECT normalized_destination, received_timestamp FROM sms_history_messages INNER JOIN sms_history_participants ON sms_history_messages.sender_id = sms_history_participants._id WHERE message_status = 1 AND sms_history_messages.reportID = %s", (id,))
    result = mycursor.fetchall()

    x4 = []
    y4 = []
    for i in result:
        y4.append(i[0])
        x4.append(i[1]/1000) #milisec to sec

    mycursor.close()
    mydb.close()

    datas = ((x1, y1),(x2, y2),(x3, y3),(x4, y4))
    return datas


# get data for during time plot
def get_data_duration(id):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="thesis_1920_result"
        )
    mycursor = mydb.cursor()

    mycursor.execute("SELECT number, date, duration FROM call_history WHERE type = 1 AND reportID = %s", (id,))
    result = mycursor.fetchall()

    x1 = []
    y1 = []
    for i in result:
        y1.append(i[0]+' '+datetime.datetime.fromtimestamp(i[1]/1000).strftime('%Y-%m-%d %I:%M:%S%p'))
        x1.append(i[2]/1000) #milisec to sec

    mycursor.execute("SELECT number, date, duration FROM call_history WHERE type = 2 AND reportID = %s", (id,))
    result = mycursor.fetchall()

    x2 = []
    y2 = []
    for i in result:
        y2.append(i[0]+' '+datetime.datetime.fromtimestamp(i[1]/1000).strftime('%Y-%m-%d %I:%M:%S%p'))
        x2.append(i[2]/1000) #milisec to sec

    mycursor.close()
    mydb.close()
    datas = ((x1, y1),(x2, y2))
    return datas


# get data for map marker
def get_data_location(id):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="thesis_1920_result"
        )
    mycursor = mydb.cursor()

    mycursor.execute("SELECT number, date, geocoded_location FROM call_history WHERE type = 1 AND reportID = %s", (id,))
    result = mycursor.fetchall()

    comment1 = []
    locate1 = []
    for i in result:
        comment1.append(i[0]+'\n'+datetime.datetime.fromtimestamp(i[1]/1000).strftime('%Y-%m-%d %I:%M:%S%p'))
        locate1.append(i[2]) #milisec to sec

    mycursor.execute("SELECT number, date, geocoded_location FROM call_history WHERE type = 2 AND reportID = %s", (id,))
    result = mycursor.fetchall()

    comment2 = []
    locate2 = []
    for i in result:
        comment2.append(i[0]+'\n'+datetime.datetime.fromtimestamp(i[1]/1000).strftime('%Y-%m-%d %I:%M:%S%p'))
        locate2.append(i[2]) #milisec to sec

    mycursor.close()
    mydb.close()
    datas = ((comment1, locate1),(comment2, locate2))
    return datas


# draw freq graph
def draw_freq_plot(values):
    x1 = values[0][0]
    y1 = values[0][1]
    x2 = values[1][0]
    y2 = values[1][1]
    x3 = values[2][0]
    y3 = values[2][1]
    x4 = values[3][0]
    y4 = values[3][1]
    secs1 = mdate.epoch2num(x1)
    secs2 = mdate.epoch2num(x2)
    secs3 = mdate.epoch2num(x3)
    secs4 = mdate.epoch2num(x4)

    datas = ((secs1, y1),(secs2, y2),(secs3, y3),(secs4, y4))
    colors = ("red", "blue","green","orange")
    groups = ("call income", "call outcome", "messages from", "messages to")

    fig, ax = plt.subplots()
    for data, color, group in zip(datas, colors, groups):
        x, y = data
        ax.plot_date(x, y, alpha=0.8, c=color, label=group)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(color='grey', linestyle='-', linewidth=0.25, alpha=0.5)
    ax.legend(groups)
    date_fmt = '%Y-%m-%d %I:%M:%S%p'
    date_formatter = mdate.DateFormatter(date_fmt)
    ax.xaxis.set_major_formatter(date_formatter)
    fig.autofmt_xdate()

    plt.title('Call and Message frequency')
    plt.xlabel('date')
    plt.ylabel('numbers')
    plt.show()


# draw timing graph
def draw_duration_plot(values):
    x1 = values[0][0]
    y1 = values[0][1]
    x2 = values[1][0]
    y2 = values[1][1]

    y_pos = np.arange(len(y1+y2))
    plt.barh(y_pos, x1+x2)
    plt.yticks(y_pos, y1+y2)


    plt.grid(color='grey', linestyle='-', linewidth=0.25, alpha=0.5)
    plt.title('Call times')
    plt.show()


# draw map
def draw_map(values):
    # save [long, lat] but load [lat, long]
    # Ex: locations = "[ 10.8902459, 106.8016362 ]"
    comments1 = values[0][0]
    locations1 = values[0][1]
    comments2 = values[1][0]
    locations2 = values[1][1]
    
    avg = locations1 + locations2
    avg_lat = 0
    avg_long = 0
    for i in avg:
        tmp = i.split(' ')
        lat = float(tmp[2])
        long = float(tmp[1][:-1])
        avg_lat += lat
        avg_long += long
    avg_lat /= len(avg)
    avg_long /= len(avg)

    my_map = folium.Map(location = [avg_lat, avg_long]) 

    for comment, location in zip (comments1, locations1):
        tmp = location.split(' ')
        lat = float(tmp[2])
        long = float(tmp[1][:-1])
        folium.Marker([lat, long], popup = comment, icon=folium.Icon(color="red")).add_to(my_map) 
    for comment, location in zip (comments2, locations2):
        tmp = location.split(' ')
        lat = float(tmp[2])
        long = float(tmp[1][:-1])
        folium.Marker([lat, long], popup = comment, icon=folium.Icon(color="blue")).add_to(my_map) 
    my_map.save(" my_map.html ")  


# create processes
def run_draw_freq_plot(id):
    values = get_data_freq(id)
    print (values)
    draw_freq_plot(values)


def run_draw_duration_plot(id):
    values = get_data_duration(id)
    draw_duration_plot(values)


def run_draw_map(id):
    values = get_data_location(id)
    draw_map(values)


def get_message(id):
    import os
    import sys

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="thesis_1920_result"
        )
    mycursor = mydb.cursor()

    mycursor.execute('''SELECT full_name, display_destination, timestamp, sms_history_conversation_participants.conversation_id, message_status, text FROM sms_history_parts INNER JOIN sms_history_conversation_participants 
                    ON sms_history_parts.conversation_id = sms_history_conversation_participants.conversation_id
                    INNER JOIN sms_history_participants 
                    ON sms_history_conversation_participants.participant_id = sms_history_participants._id 
                    INNER JOIN sms_history_messages
                    ON sms_history_parts.conversation_id = sms_history_messages.conversation_id WHERE sms_history_parts.reportID = %s''', (id,))
    result = mycursor.fetchall()
    for i in result:
        if i[4] == 100:
            # os.system('color 4') # change color here
            print (i[5])
        else:
            # os.system('color 5') # change color here
            print (i[5])


def main():
    # create process
    p = []
    if args.plot:
        p1 = multiprocessing.Process(target=run_draw_freq_plot, args=(args.report,))
        p2 = multiprocessing.Process(target=run_draw_duration_plot, args=(args.report,))
        p.append(p1)
        p.append(p2)
    if args.map:
        p3 = multiprocessing.Process(target=run_draw_map, args=(args.report,))
        p.append(p3)
    if args.showmess:
        p4 = multiprocessing.Process(target=get_message, args=(args.report,))
        p.append(p4)
    for i in p:
        i.start()
    for i in p:
        i.join()
    print("Done!")


if __name__ == "__main__":
    main()