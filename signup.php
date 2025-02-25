<?php
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: POST");
header("Access-Control-Allow-Headers: Content-Type");

include 'db_config.php';

// Get POST data
$data = json_decode(file_get_contents("php://input"), true);
$username = $data['username'];
$email = $data['email'];
$phone = $data['phone'];
$password = password_hash($data['password'], PASSWORD_BCRYPT);

// Check for existing username, email, or phone
$query = "SELECT * FROM users WHERE username=:username OR email=:email OR phone=:phone";
$stmt = $conn->prepare($query);
$stmt->bindParam(':username', $username);
$stmt->bindParam(':email', $email);
$stmt->bindParam(':phone', $phone);
$stmt->execute();
if ($stmt->rowCount() > 0) {
    echo json_encode(["status" => "error", "message" => "Username, Email, or Phone already exists."]);
    exit();
}

// Insert new user
$query = "INSERT INTO users (username, email, phone, password) VALUES (:username, :email, :phone, :password)";
$stmt = $conn->prepare($query);
$stmt->bindParam(':username', $username);
$stmt->bindParam(':email', $email);
$stmt->bindParam(':phone', $phone);
$stmt->bindParam(':password', $password);

if ($stmt->execute()) {
    echo json_encode(["status" => "success", "message" => "User created successfully."]);
} else {
    echo json_encode(["status" => "error", "message" => "Failed to create user."]);
}
?>
