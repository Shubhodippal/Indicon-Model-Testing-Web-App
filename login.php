<?php
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: POST");
header("Access-Control-Allow-Headers: Content-Type");

include 'db_config.php';

// Get POST data
$data = json_decode(file_get_contents("php://input"), true);
$email = $data['email'];
$password = $data['password'];

// Check if user exists
$query = "SELECT * FROM users WHERE email=:email";
$stmt = $conn->prepare($query);
$stmt->bindParam(':email', $email);
$stmt->execute();

if ($stmt->rowCount() > 0) {
    $user = $stmt->fetch(PDO::FETCH_ASSOC);
    if (password_verify($password, $user['password'])) {
        echo json_encode(["status" => "success", "message" => "Login successful.", "username" => $user['username'], "email" => $user['email']]);
    } else {
        echo json_encode(["status" => "error", "message" => "Invalid password."]);
    }
} else {
    echo json_encode(["status" => "error", "message" => "User not found."]);
}
?>