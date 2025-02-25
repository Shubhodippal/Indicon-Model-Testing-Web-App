<?php
$host = "sdb-80.hosting.stackcp.net";
$db_name = "SERS_db-353038356182";
$username = "SERS_db-353038356182";
$password = "sers_demo";

try {
    $conn = new PDO("mysql:host=$host;dbname=$db_name", $username, $password);
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch (PDOException $e) {
    echo "Connection failed: " . $e->getMessage();
}
?>
