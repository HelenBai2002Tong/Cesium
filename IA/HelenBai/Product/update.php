<?php
session_start();
include('testphpdb.php');
//set the time zone as where I am
date_default_timezone_set("Asia/Shanghai");
$sender=$_SESSION['username'];
$title = $_POST['title'];
$description = $_POST['description'];
$olddate=$_SESSION['date'];
$newdate = date("Y-m-d h:i:sa");//get the date and time now
//modify the posts in the database(change the time as well)
$sql = "UPDATE posts SET title='$title', description='$description', Date = '$newdate' WHERE sender='$sender' and Date='$olddate'";
$result1 = mysqli_query($connection,$sql);
//remind the user the result
if (!$result1) {
    echo "<script>alert('Please try again')</script>";
    } else {
    echo "<script>alert('Successful edit!');parent.location.href='profile1.php';</script>";
}
?>