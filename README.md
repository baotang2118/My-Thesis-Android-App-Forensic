# My-Thesis-Android-App-Forensic
This is my thesis project
#README
##Cấu trúc thư mục
ROOT/
--ANDROID_APP_FORENSIC/
----SETUP/
------Project_Thesis_1920.zip
----SOURCE/
------Project_Thesis_1920/
--------Angular/
--------php/
--------python3/
--BAO CAO/
----ABS/
------video_KL.mp4
----DOC/
------UIT_BaoCaoKL.docx
----PDF/
------UIT_BaoCaoKL.pdf
--REF/
----[1]. Abdullah Azfar, Kim-Kwang Raymond Choo, Lin Liu (2016), An Android Social App Forensics Adversary Model.pdf
----[4]. Animesh Kumar Agrawal, Aman Sharma, Pallavi Khatri (2019), Android Forensics Tools and Techniques for Manual Data Extraction.pdf
----[5]. Bernard Chukwuemeka Ogazi-Onyemaechi, Ali Dehghantanha, Kim-Kwang Raymond Choo (2017), Performance of Android Forensics Data Recovery Tools.pdf
----[6]. Cosimo Anglano (2014), Forensic analysis of WhatsApp Messenger on Android smartphones.pdf
----[7]. F.Karpisek, I.Baggili, F.Breitingerb (2015), WhatsApp network forensics Decrypting and understanding the WhatsApp call signaling messages.pdf
----[8]. Joe Kong (2016), Data Extraction on MTK-based Android Mobile Phone Forensics.pdf
----[9]. Nihar Ranjan Roy, Anshul Kanchan Khanna, Leesha Aneja (2016), Android phone forensic Tools and techniques.pdf
--SOFT/
----androguard.exe
----jadx-1.0.0.exe
----sleuthkit.exe
--README


##Hướng dẫn
Các tài liệu được lưu theo cấu trúc thư mục trên
- Thư mục ANDROID_APP_FORENSIC gồm hai thư mục
  - SETUP: chứa các file dùng để install chương trình
  - SOURCE: chứa các file mã nguồn
- Thư mục BAO CAO: chứa các tập tin tài liệu văn bản của khóa luận, với các thư mục con được tổ chức như sau:
  - DOC: chứa tài liệu dạng .DOC.
  - PDF: chứa tài liệu dạng .PDF.
  - ABS: chứa báo cáo khóa luận gồm báo cáo dạng .PPT (slide), .AVI (clip demo)
- Thư mục REF: chứa các tài liệu dùng để tham khảo khi thực hiện khóa luận.
- Thư mục SOFT: chứa các phần mềm liên quan trong quá trình thực hiện khóa luận.
- README chứa hướng dẫn sử dụng cho việc sử dụng đĩa CD, có đầy đủ thông tin liên lạc với nhóm tác giả (email, điện thoại).

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

Dù trong CD đã có file cài đặt, nhưng chưa chứa các config môi trường, hơn nữa file máy ảo khá nặng nên không thể chép vào trong CD được.


##Nhóm tác giả
Tăng Đức Bảo -15520043
email: 15520043@gm.uit.edu.vn
0339688830
Khưu Ngọc Anh - 15520017
email: 15520017@gm.uit.edu.vn
0354400648