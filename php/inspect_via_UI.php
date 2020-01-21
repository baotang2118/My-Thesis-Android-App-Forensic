<?php

	if (isset($_GET['view_queue'])){
		$conn = mysqli_connect("localhost", "root", "", "thesis_1920_waiting_queue");
		if ($conn-> connect_error){
			die("Connection failed:". $conn-> connect_error);
		}
		$queue = [];
		if($results = $conn->query('SELECT id, cmd, status FROM queue WHERE status IS NULL')){
			$cr = 0;
			while ($row = $results->fetch_assoc()) {
				$queue[$cr]['id'] = $row['id'];
				$queue[$cr]['cmd'] = $row['cmd'];
				$queue[$cr]['status'] = $row['status'];
				$cr++;
			}
			echo json_encode(['data'=>$queue]);
		}
		$conn->close();
		exit;
	}


	$tool_path = "cd C:\\Project_Thesis_1920\\python\\ && C:\\Project_Thesis_1920\\python\\tools_android_apk_finfo_collection.py --input ";

	if (isset($_POST['absolute_path'])){
		$conn = mysqli_connect("localhost", "root", "", "thesis_1920_waiting_queue");
		if ($conn-> connect_error){
			die("Connection failed:". $conn-> connect_error);
		}
		$absolute_path = $conn -> real_escape_string($_POST['absolute_path']);
		$cmd =  $conn -> real_escape_string($tool_path) . $absolute_path;
		$source = $absolute_path;
		$sql = "INSERT INTO queue(cmd, source) VALUES('$cmd', '$source')";

		if (!mysqli_query($conn, $sql)){
			echo "Error: " . $sql . "<br>" . mysqli_error($conn);
		}
		$conn->close();
		exit;
	}
?>