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

$job_skill = mysqli_real_escape_string($conn,$_GET["table_name"]);
$max_results = mysqli_real_escape_string($conn,$_GET["number_of_results"]);
$city = mysqli_real_escape_string($conn,$_GET["city_name"]);
$skill_type = mysqli_real_escape_string($conn,$_GET["skill_type"]);

try{
  $max_results = intval($max_results);
}
catch (Exception $e){
  $max_results = 10;
}

if($max_results == 0){
  $max_results = 10;
}

$all_matches = [];

$sql = "CALL sp_get_count_of_all_skills_in_city_corresponding_job_skill('" . $skill_type . "', '" . $city . "'," . $max_results . ",'" . $job_skill . "')";

$result = $conn->query($sql);

if ($result->num_rows > 0) {
    while($row = $result->fetch_assoc()) {

        $number_of_jobs = $row["TOTALCOUNT"];
        $skill_being_counted = $row["job_skill"];
        $all_matches[$skill_being_counted] = $number_of_jobs;
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

arsort($all_matches);

foreach ($all_matches as $skill_description => $count){
  echo $record_seperator . "{\"c\":[{\"v\":\"" . $skill_description . "\",\"f\":null},{\"v\":" . $count . ",\"f\":null}]}";
  $record_seperator = ",";
}

echo "]";
echo "}";

?>
