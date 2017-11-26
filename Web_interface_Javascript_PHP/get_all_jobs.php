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

try{
$max_results = $_GET["number_of_results"];
  $max_results = intval($max_results);
}
catch (Exception $e){
  $max_results = 10;
}

$city = $_GET["city_name"];

if($max_results == 0){
  $max_results = 10;
}

$all_matches = [];

$sql = "SELECT COUNT(*) as TOTALCOUNT, job_skill FROM `job_table` WHERE city = '" . $city . "' GROUP BY job_skill";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    while($row = $result->fetch_assoc()) {

        $next_value = $row["TOTALCOUNT"];
        $all_matches[$row["job_skill"]] = $next_value;
    }

} else {
    //echo "0 results";
}

echo "{";

echo " \"cols\": [
        {\"id\":\"\",\"label\":\"Skill decription\",\"pattern\":\"\",\"type\":\"string\"},
        {\"id\":\"\",\"label\":\"Amount of jobs\",\"pattern\":\"\",\"type\":\"number\"}
      ],";

echo "\"rows\": [";

$record_seperator = "";

$counter = 0;

arsort($all_matches);

foreach ($all_matches as $skill_description => $count){
  if($counter < $max_results){
  echo $record_seperator . "{\"c\":[{\"v\":\"" . $skill_description . "\",\"f\":null},{\"v\":" . $count . ",\"f\":null}]}";
  $record_seperator = ",";
  $counter++;
} else{
  break;
}
}

echo "]";
echo "}";


?>
