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
$max_results = $_GET["number_of_results"];
$city = $_GET["city_name"];

try{
  $max_results = intval($max_results);
}
catch (Exception $e){
  $max_results = 10;
}

if($max_results == 0){
  $max_results = 10;
}

$array_for_table_names = [];

$sql = "SELECT job_skill FROM `master_table` WHERE job_skill <> '" . $firsttable . "'";
$result = $conn->query($sql);
if ($result->num_rows > 0) {
    while($row = $result->fetch_assoc()) {
        $next_value = $row["job_skill"];
        array_push($array_for_table_names,$next_value);
    }
  }

$other_tables = $array_for_table_names;

foreach($other_tables as $this_table){
$othertable = $this_table;

$sql = "SELECT COUNT(*) as TOTALCOUNT FROM `job_table` t1 INNER JOIN `job_table` t2 ON t1.url = t2.url AND t1.job_skill = '" . $firsttable . "' AND t2.job_skill = '" . $othertable . "' AND t1.city='" . $city . "'";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    while($row = $result->fetch_assoc()) {

        $next_value = $row["TOTALCOUNT"];
        $all_matches[$othertable] = $next_value;
    }

} else {
    //echo "0 results";
}
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
