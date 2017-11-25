<?php
$servername = "localhost";
$dbname = "Jobs";
$username = "";
$password = "";

$file_handle = fopen("username password file.txt", "r");
while (!feof($file_handle)) {
   $line = trim(fgets($file_handle));
   $uname_pword = explode(",",$line);
   $username = $uname_pword[0];
   $password = $uname_pword[1];
   break;
}
fclose($file_handle);

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$all_matches = [];


$firsttable = $_GET["table_name"];

$array_for_table_names = [];

$sql = "SELECT job_skill FROM `master_table` WHERE job_skill <> '" . $firsttable . "'";
$result = $conn->query($sql);
$started = 0;
echo "{\"names\":[";
if ($result->num_rows > 0) {
    while($row = $result->fetch_assoc()) {
        $next_value = $row["job_skill"];
        if($started){
          echo ",";
        }
        $started = 1;
        echo "\"" . $next_value . "\"";
    }
  }
echo "]}";

  ?>
