<?php
include 'db_connection_start.php';

try{
$max_results = $_GET["number_of_results"];
  $max_results = intval($max_results);
}
catch (Exception $e){
  $max_results = 10;
}

$city = mysqli_real_escape_string($conn,$_GET["city_name"]);
$skill_type = mysqli_real_escape_string($conn,$_GET["skill_type"]);

if($max_results == 0){
  $max_results = 10;
}

$all_matches = [];
$sql = "CALL sp_get_count_of_all_jobs('" . $city . "', '" . $skill_type . "', " . $max_results . ")";

$result = $conn->query($sql);

if ($result->num_rows > 0) {
    while($row = $result->fetch_assoc()) {

        $next_value = $row["TOTALCOUNT"];
        $all_matches[$row["job_skill"]] = $next_value;
    }

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
