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

$count_total = 0;

$firsttable = mysqli_real_escape_string($conn,$_GET["table_name"]);
$city = mysqli_real_escape_string($conn,$_GET["city_name"]);

$sql = "CALL sp_get_count_of_all_jobs_in_city('" . $firsttable . "', '" . $city . "')"; 
$result = $conn->query($sql);
if ($result->num_rows > 0) {
    while($row = $result->fetch_assoc()) {
        $next_value = $row["COUNT(*)"];
        $count_total = $next_value;
    }
  }

  echo "{\"count\":\"" . $count_total . "\"}";

?>
