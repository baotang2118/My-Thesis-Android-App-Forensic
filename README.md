# My-Thesis-Android-App-Forensic
This is my thesis project
#README

Cách dùng công cụ như sau:
- Cài các phầm mềm cần thiết
  - Python 3
  - Androiguard (cài từ source code), matplotlib, folium
  - Nodejs, Angularjs
  - XAMPP
- Copy toàn bộ thư mục đồ án vào nơi tùy ý
- Chạy file cmd_databases.py, chỉ chạy một lần duy nhất để tạo database
- Chạy file demo_preprare_datasheet.py để tạo datasheet, người dùng phải tự điền thông tin vào
- File delete.bat dùng để reset chương trình, xóa hết databases và các tệp tin tạm (cần phải chỉnh sửa đường dẫn trong nội dung cho phù hợp)
- Tạo một thư mục mới tên là api vào trong đường dẫn htdocs của XAMPP
- Copy toàn bộ code trong thư mục php của đồ án cho vào trong folder /api này
- Bật Apache, MySQL trong XAMPP lên, dùng trình duyệt di chuyển đến đường dẫn vừa tạo (Ví dụ: http://localhost/api/), chọn get_report.php, thấy dữ liệu json trả về mà không báo lỗi là thành công.

Để phân tích file:
- Dùng command Prompt hoặc PowerShell:
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
