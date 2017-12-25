<?php
include 'db_connection_start.php';

echo "{";
echo "\"names\":[";
$sql = "CALL sp_get_all_cities()";
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
