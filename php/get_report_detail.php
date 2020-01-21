<?php
	$conn = mysqli_connect("localhost", "root", "", "thesis_1920_result");
	if ($conn-> connect_error){
			die("Connection failed:". $conn-> connect_error);
		}

	if(isset($_GET["report"])){
		$apk_full_report = [];
		$reportID = $_GET["report"];
		$sql_apk_info_detail = "SELECT obj_id, name, mtime, atime, ctime, crtime, size, appName, packageName, androidversionCode, androidversionName, path2Icon, cert, MD5, SHA1, SHA256, sendBroadcast, onReceive, startService, onHandleIntent, startActivity, getIntent FROM object INNER JOIN apk_files_info on object.obj_id = apk_files_info.apk_id INNER JOIN apk_files_detail on object.obj_id = apk_files_detail.apk_id WHERE source = $reportID;";
		$results_info_detail = $conn->query($sql_apk_info_detail);
		$cr = 0;
		while ($row_info_detail = $results_info_detail->fetch_assoc()) {
			$apk_full_report[$cr]['obj_id'] = $row_info_detail['obj_id'];
			$apk_full_report[$cr]['name'] = mb_convert_encoding($row_info_detail['name'], "UTF-8", "Windows-1252");
			
			$apk_full_report[$cr]['mtime'] = $row_info_detail['mtime'];
			$apk_full_report[$cr]['atime'] = $row_info_detail['atime'];
			$apk_full_report[$cr]['ctime'] = $row_info_detail['ctime'];
			$apk_full_report[$cr]['crtime'] = $row_info_detail['crtime'];
			$apk_full_report[$cr]['size'] = $row_info_detail['size'];

			$apk_full_report[$cr]['appName'] = mb_convert_encoding($row_info_detail['appName'], "UTF-8", "Windows-1252");
			$apk_full_report[$cr]['packageName'] = $row_info_detail['packageName'];
			$apk_full_report[$cr]['androidversionCode'] = $row_info_detail['androidversionCode'];
			$apk_full_report[$cr]['androidversionName'] = $row_info_detail['androidversionName'];
			$apk_full_report[$cr]['path2Icon'] = $row_info_detail['path2Icon'];
			$apk_full_report[$cr]['cert'] = $row_info_detail['cert'];
			$apk_full_report[$cr]['cert'] = mb_convert_encoding($row_info_detail['cert'], "UTF-8", "Windows-1252");

			$apk_full_report[$cr]['MD5'] = $row_info_detail['MD5'];
			$apk_full_report[$cr]['SHA1'] = $row_info_detail['SHA1'];
			$apk_full_report[$cr]['SHA256'] = $row_info_detail['SHA256'];
			$apk_full_report[$cr]['sendBroadcast'] = $row_info_detail['sendBroadcast'];
			$apk_full_report[$cr]['onReceive'] = $row_info_detail['onReceive'];
			$apk_full_report[$cr]['startService'] = $row_info_detail['startService'];
			$apk_full_report[$cr]['onHandleIntent'] = $row_info_detail['onHandleIntent'];
			$apk_full_report[$cr]['startActivity'] = $row_info_detail['startActivity'];
			$apk_full_report[$cr]['getIntent'] = $row_info_detail['getIntent'];
			
			$obj_id = $row_info_detail['obj_id'];
			$apk_components = [];
			$sql_apk_components = "SELECT ComponentName, ComponentType, ExportStatus FROM apk_files_detail_components WHERE apk_id = $obj_id";

			$results_components = $conn->query($sql_apk_components);
			$cr_ = 0;
			while ($row_components = $results_components->fetch_assoc()) {
				$apk_components[$cr_]['ComponentName'] = $row_components['ComponentName'];
				$apk_components[$cr_]['ComponentType'] = $row_components['ComponentType'];
				$apk_components[$cr_]['ExportStatus'] = $row_components['ExportStatus'];
				$cr_++;
			}
			$apk_full_report[$cr]['Components'] = $apk_components;

			$apk_permissions = [];
			$sql_apk_permissions = "SELECT PermissionName FROM apk_files_detail_permissions WHERE apk_id = $obj_id";
			$results_permisisons = $conn->query($sql_apk_permissions);
			$cr__ = 0;
			while ($row_permissions = $results_permisisons->fetch_assoc()) {
				$danger = $row_permissions['PermissionName'];
				$sql_danger = "SELECT 1 FROM dangerous_permission WHERE PermissionName = substr('$danger',20)";
				$results_danger = $conn->query($sql_danger);
				$tmp = $results_danger->fetch_assoc();
				if ($tmp)
					$apk_permissions[$cr__]['PermissionName'] = $row_permissions['PermissionName'].'*';
				else
					$apk_permissions[$cr__]['PermissionName'] = $row_permissions['PermissionName'];
				$cr__++;
			}
			$apk_full_report[$cr]['Permissions'] = $apk_permissions;

			$apk_mails = [];
			$sql_apk_mails = "SELECT email FROM apk_files_email WHERE apk_id = $obj_id";

			$results_mails = $conn->query($sql_apk_mails);
			$cr___ = 0;
			while ($row_mails = $results_mails->fetch_assoc()) {
				$apk_mails[$cr___]['email'] = $row_mails['email'];
				$cr___++;
			}
			$apk_full_report[$cr]['emails'] = $apk_mails;

			$apk_urls = [];
			$sql_apk_urls = "SELECT url FROM apk_files_url WHERE apk_id = $obj_id";

			$results_urls = $conn->query($sql_apk_urls);
			$cr____ = 0;
			while ($row_urls = $results_urls->fetch_assoc()) {
				$apk_urls[$cr____]['url'] = $row_urls['url'];
				$cr____++;
			}
			$apk_full_report[$cr]['urls'] = $apk_urls;

			$apk_ips = [];
			$sql_apk_ips = "SELECT ip FROM apk_files_ip WHERE apk_id = $obj_id";

			$results_ips = $conn->query($sql_apk_ips);
			$cr_____ = 0;
			while ($row_ips = $results_ips->fetch_assoc()) {
				$apk_ips[$cr_____]['ip'] = $row_ips['ip'];
				$cr_____++;
			}
			$apk_full_report[$cr]['ips'] = $apk_ips;

			$recovered_file = [];
			$package_name = $row_info_detail['packageName'];
			$sql_recovered_file = "SELECT link_to_file, file_name FROM recovered_file WHERE reportID = $reportID AND package_name ='$package_name'";
			$results_recovered_file = $conn->query($sql_recovered_file);
			$cr_recovered = 0;
			while ($row_recovered_file = $results_recovered_file->fetch_assoc()) {
				$recovered_file[$cr_recovered]['link_to_file'] = $row_recovered_file['link_to_file'];
				$recovered_file[$cr_recovered]['file_name'] = $row_recovered_file['file_name'];
				$cr_recovered++;
			}
			$apk_full_report[$cr]['recovered_file'] = $recovered_file;

			$cr++;

		}
		echo json_encode(['data'=>$apk_full_report], JSON_UNESCAPED_UNICODE );
	}
	$conn->close();
?>