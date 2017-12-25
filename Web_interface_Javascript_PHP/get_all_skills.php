<?php

include 'db_connection_start.php';

$all_matches = [];


$firsttable = mysqli_real_escape_string($conn,$_GET["table_name"]);

$array_for_table_names = [];

$sql = "CALL sp_get_all_skills ('" . $firsttable . "')";
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
