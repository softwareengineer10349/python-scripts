<?php

$servername = "";
$dbname = "";
$username = "";
$password = "";

$file_handle = fopen("username password file.txt", "r");
while (!feof($file_handle)) {
   $line = trim(fgets($file_handle));
   $uname_pword = explode(",",$line);
   $username = $uname_pword[0];
   $password = $uname_pword[1];
   $servername = $uname_pword[2];
   $dbname = $uname_pword[3];
   break;
}
fclose($file_handle);

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

?>
