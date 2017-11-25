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
echo "{";
echo "\"names\":[";
$sql = "SELECT DISTINCT city FROM `job_table`";
$result = $conn->query($sql);
$record_seperator = "";
if ($result->num_rows > 0) {
    while($row = $result->fetch_assoc()) {
      echo $record_seperator . "\"" . $row["city"] . "\"";
      $record_seperator = ",";
    }
  }

echo "]";
echo "}";

?>
