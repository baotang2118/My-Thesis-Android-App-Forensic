# My-Thesis-Android-App-Forensic
This is my thesis project, we study Android phone forensic topic and focus only on the user app, which means we skip default app which come from OEM. The input can be an raw disk image or a rooted phone.

## How to use this app:
- Install basic tools
  - Python 3
  - mysql-connector, Androiguard, matplotlib, folium
  - Nodejs, Angularjs
  - XAMPP
- Clone and exact project
- Run `cmd_databases.py`, run only once to create the database
- Run `demo_preprare_datasheet.py` to create datasheet, user has to define the app and it's external directory's name by themselves
- To reset app: run `delete.bat`, this action will delete all databases and temporary file. **User has to adjust temporary file's localtion inside the code**
- Add new folder named `api` in htdocs (*Ex:* /xampp/htdocs/api/)
- Copy all file in folder `php` to folder `/api`
- Turn on Apache, MySQL in XAMPP, use your browser to browse to `http://localhost/api/`, click `get_report.php`, if you saw the returned data is in json format without error, you'd complete installing process.

To analyze:
- By using command Prompt or PowerShell:
  + cd into `python` folder
  + Type `python tools_android_apk_finfo_collection.py --input <link_to_img>`
- By using web UI:
  + Run `web_binding.py` by command Prompt or PowerShell
  + Turn on Apache, MySQL in XAMPP
  + Use your browser to browse to `localhost:4200`, fill file'path in form (*Ex:* E:\raw_image_disk\abcxyz.dd), click `Analysis`
  + Incompleted Analysis will come below
  + Completed Analysis will appear above afer finish, you can track it on command Prompt or PowerShell

**Note 1:** the file format must be raw, dd, iso or img, if not, you have to use VboxManage to convert. Type:
```
VBoxManage.exe clonehd input.vdi Output.img --format raw
```
**Note 2** at the first running time, `web_binding.py` must be run first so it can create it's own table in DB

To clone Android phone storage:
- Run `clone.py` in "tools" directory, type: `python clone.py --name <link_to_img>`, it'll automatically check adb and connection
- The output will be located at the same folder with clone.py

**Note 3:** adb client must be replaced to suite the adb server (version)

To view web report
- Turn on Apache in XAMPP or run `run_xampp.bat`
- Run `run_angularjs.bat`
- Browse to `localhost:4200`

To visualize the gathered information:
- Copy report's id from web report or web_binding.py's window
- Run `python data_visualate.py --plot --map --report <report_id>`
- Currently, this app support only android 7.0

## Results
update later

