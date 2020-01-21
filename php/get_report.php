<?php
	$conn = mysqli_connect("localhost", "root", "", "thesis_1920_result");
	if ($conn-> connect_error){
			die("Connection failed:". $conn-> connect_error);
		}

	$reports = [];
	if($results = $conn->query('SELECT * FROM data_source WHERE total_times IS NOT NULL')){
		$cr = 0;
		while ($row = $results->fetch_assoc()) {
			$reports[$cr]['obj_id'] = $row['obj_id'];
			$reports[$cr]['current_times'] = $row['current_times'];
			$reports[$cr]['total_times'] = $row['total_times'];
			$reports[$cr]['type'] = $row['type'];
			$reports[$cr]['size_in_bytes'] = $row['size_in_bytes'];
			$reports[$cr]['section'] = $row['section'];
			$reports[$cr]['path_to_source'] = $row['path_to_source'];
			switch ($row['SdkVersion']) {
				case 14:
					$reports[$cr]['AndroidVersion'] = "4.0";
					break;
				case 15:
					$reports[$cr]['AndroidVersion'] = "4.0";
					break;
					case 16:
					$reports[$cr]['AndroidVersion'] = "4.1";
					break;
				case 17:
					$reports[$cr]['AndroidVersion'] = "4.2";
					break;
				case 18:
					$reports[$cr]['AndroidVersion'] = "4.3";
					break;
				case 19:
					$reports[$cr]['AndroidVersion'] = "4.4";
					break;
				case 21:
					$reports[$cr]['AndroidVersion'] = "5.0";
					break;
				case 22:
					$reports[$cr]['AndroidVersion'] = "5.1";
					break;
				case 23:
					$reports[$cr]['AndroidVersion'] = "6.0";
					break;
				case 24:
					$reports[$cr]['AndroidVersion'] = "7.0";
					break;
				case 25:
					$reports[$cr]['AndroidVersion'] = "7.1";
					break;
				case 26:
					$reports[$cr]['AndroidVersion'] = "8.0";
					break;
				case 27:
					$reports[$cr]['AndroidVersion'] = "8.1";
					break;
				case 28:
					$reports[$cr]['AndroidVersion'] = "9";
					break;
				case 29:
					$reports[$cr]['AndroidVersion'] = "10";
					break;
				default:
					$reports[$cr]['AndroidVersion'] = "N/A";
					break;
			}
			$cr++;
		}
		echo json_encode(['data'=>$reports]);
	}
	$conn->close();
?>