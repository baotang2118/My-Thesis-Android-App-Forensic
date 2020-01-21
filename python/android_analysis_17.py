#!/usr/bin/env python

from __future__ import print_function
from androguard.cli import androlyze_main
from androguard.core.androconf import *
from androguard.misc import *
import os
import json
import subprocess
import cmd_databases
import sqlstorehash

# GET neccessary info like below
LIST_NAME_METHODS = ["sendBroadcast", "onReceive", "startService", "onHandleIntent", "startActivity", "getIntent"];
LIST_NAME_OVERVIEW = ["STT", "APK Name", "appName", "packageName", "androidversionCode", "androidversionName",
                      "pathIcon()", "cert"]
LIST_HEADER = ["STT", "APK Name"] + LIST_NAME_METHODS + ["Component Type", "Component Name", "Exported Status",
                                                         "getPermissions"]


class AndroidInfo:
    def __init__(self, tableCountMethod, tableOverview):
        self.tableCountMethod = tableCountMethod
        self.tableOverview = tableOverview


def count_Method_APK(methodName, listMethods):
    count = 0
    newlist = list()
    for element in listMethods:
        newlist.append(element.__repr__())
    for l in newlist:
        if methodName in l:
            count += 1
    return count


def attribute_Component(analysis_Obj):
    manifest_Obj = analysis_Obj.get_android_manifest_xml()
    application_Tag = manifest_Obj.findall("application")
    latrr = list()
    list_Component = list()
    dem = 0
    for childs in application_Tag:
        for child in childs:
            keys = list()
            keys = child.keys()
            newdict = dict()
            list_Component.append(child.tag)
            for key in keys:
                lsplit = key.split("}")
                newdict[lsplit[-1]] = child.get(key)
            latrr.append(newdict)
    return latrr, list_Component


def get_Atrribute(listDict):
    list_Name_Of_Component = list()
    list_Exported_Of_Component = list()
    for dictt in listDict:
        list_Name_Of_Component.append(dictt.get('name'))
        list_Exported_Of_Component.append(dictt.get('exported'))
    return list_Name_Of_Component, list_Exported_Of_Component


def get_List_Contens(path, nameAPK):
    list_Count_Methods = list()
    list_Infor_Overview = list()
    try:
        a, d, dx = AnalyzeAPK(path)
        listMethods = list(dx.get_methods())
        # list_Count_Methods = list()
        # list_Infor_Overview = list()
        list_Count_Methods.append(nameAPK)
        # ####################################
        #   baotd added hash function here
        # ####################################
        print(path)
        MD5, SHA1, SHA256 = sqlstorehash.hashMd5Sha1Sha256(path)
        list_Count_Methods.append(MD5)
        list_Count_Methods.append(SHA1)
        list_Count_Methods.append(SHA256)
        # ####################################
        #   This is the end of hash function
        # ####################################
        for i in range(0, len(LIST_NAME_METHODS)):
            list_Count_Methods.append(count_Method_APK(LIST_NAME_METHODS[i], listMethods))
        atrrs, components = attribute_Component(a)
        names, exports = get_Atrribute(atrrs)
        list_Count_Methods.append(components)
        list_Count_Methods.append(names)
        list_Count_Methods.append(exports)
        list_Count_Methods.append(a.get_permissions())
        ######
        list_Infor_Overview.append(nameAPK)
        if a.get_app_name():
            list_Infor_Overview.append(a.get_app_name())
        else:
            list_Infor_Overview.append("N/A")        
        list_Infor_Overview.append(a.get_package())
        list_Infor_Overview.append(a.get_androidversion_code())
        list_Infor_Overview.append(a.get_androidversion_name())
        # baotd added code here
        # C:\Project_Thesis_1920\python\..\result\05-12-2019-16-36\extracted_apks\com.estrongs.android.pop-1\resources\res
        if a.get_app_icon():
            list_Infor_Overview.append("{}\\resources\\".format(path[20:-4]) + a.get_app_icon())
        else:
            list_Infor_Overview.append("N/A")
        batcmd = "androguard sign --all --show " + path
        result = subprocess.check_output(batcmd, shell=True).decode("utf-8").replace("\r", "")
        list_Infor_Overview.append(result)
        ##list_Infor_Overview.append(dx.get_classes())
        # print(list_Infor_Overview)
    except:
        for i in range(0, len(LIST_NAME_METHODS)):
            list_Count_Methods.append("Failed!")
    return list_Count_Methods, list_Infor_Overview


def get_Path_Files(pathFolder):
    Fjoin = os.path.join
    lapkname = os.listdir(pathFolder)
    list_Of_Path_Files = [Fjoin(pathFolder, f) for f in os.listdir(pathFolder)]
    return list_Of_Path_Files, lapkname


def map_List_Methods(pathFolder):
    lspath, lsnameAPK = get_Path_Files(pathFolder)
    newlistCount = list()
    newlistOver = list()
    newlistCount.append(LIST_HEADER)
    newlistOver.append(LIST_NAME_OVERVIEW)
    i = 1
    for (lp, ln) in zip(lspath, lsnameAPK):
        ltemp, otemp = get_List_Contens(lp, ln)
        ltemp.insert(0, i)
        otemp.insert(0, i)
        newlistCount.append(ltemp)
        newlistOver.append(otemp)
        print("Completed " + str(round(i / float(len(lspath)) * 100)) + "%.")
        i = i + 1
    obj = AndroidInfo(newlistCount, newlistOver)
    # print(newlistOver)
    return newlistOver, obj

    # ####################################
    #   baotd added load db function here
    # ####################################


# Load info to databases with correct object id
def load_on_db(dir, apkslist):
    info, ob = map_List_Methods(dir + "\\extracted_apks")
    y = json.dumps(ob.__dict__)
    print(info)
    cmd_databases.insert_apk_files_info(info, apkslist)
    print(y)
    cmd_databases.insert_apk_files_detail(y, apkslist)
    # ####################################
    #   This is the end of load db function
    # ####################################
