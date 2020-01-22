# My-Thesis-Android-App-Forensic
This is my thesis project, we study Android phone forensic topic and focus only on the user app, which means we skip default app which come from OEM. The input can be an raw disk image or a rooted phone.

How to use this app:
- Install basic tools
  - Python 3
  - mysql-connector, Androiguard, matplotlib, folium
  - Nodejs, Angularjs
  - XAMPP
- Clone and exact project
- Run cmd_databases.py, run only once to create the database
- Run demo_preprare_datasheet.py to create datasheet, user has to define the app and it's external directory's name by themselves
- To reset app: run delete.bat, this action will delete all databases and temporary file (user has to adjust temporary file's localtion inside the code)
- Add new folder named "api" in htdocs (Ex: /xampp/htdocs/api/)
- Copy all file in folder php to folder /api
- Turn on Apache, MySQL in XAMPP, use your browser to browse to http://localhost/api/, click get_report.php, if you saw the return data is in json format without error, you'd complete installing process.

To analyze:
- By using command Prompt or PowerShell:
  + di chuyển vào trong thư mục chứa source code python của project
  + Gõ python tools_android_apk_finfo_collection.py --input <ten_img>
- Dùng giao diện web:
  + Chạy file web_binding.py bằng command Prompt hoặc PowerShell
  + Bật Apache, MySQL trong XAMPP lên
  + Dùng trình duyệt vào đường dẫn localhost:4200, điền đường dẫn đến file vào (ví dụ: E:\raw_image_disk\abcxyz.dd), chọn Analysis
  + Danh sách hàng chờ được hiện ra ở bảng dưới
  + Danh sách file đã phân tích xong được hiện ra ở bảng trên

Chú ý 1: Nếu định dạng bản sao chưa phải là raw, dd, iso hoặc img thì ta phải dùng công cụ VboxManage để chuyển đổi. Cú pháp như sau:
[VBoxManage.exe clonehd input.vdi Output.img --format raw]
Chú ý 2: Trong lần chạy đầu tiên, phải bật web_binding.py trước để nó khởi tạo table cho DB

Để clone dữ ổ cứng điện thoại
- Chạy file clone.py trong thư mục tools với cú pháp python clone.py --name <ten_img>, phần mềm sẽ tự động check công cụ adb và kết nối điện thoại
- File output nằm cùng thư mục với file clone.py

Chú ý 3: Phải thay đổi version adb client cho phù hợp với version adb server

Để xem web report
- Bật Apache trong XAMPP lên hoặc chạy file run_xampp.bat
- Chạy file run_angularjs.bat
- Dùng trình duyệt vào đường dẫn localhost:4200

Để mô hình hóa dữ liệu:
- Copy id của report trong qua trình phân tích
- Chạy file data_visualate.py --plot --map --report <report id>
