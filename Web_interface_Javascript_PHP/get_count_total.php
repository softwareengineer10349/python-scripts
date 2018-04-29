<?php
include 'db_connection_start.php';

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
