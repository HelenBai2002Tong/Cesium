<?php
include('testphpdb.php');
include("profile1.php");
$sender=$_SESSION['username'];//get the name of the sender
$time=$_GET['date'];//get which post to be deleted
//delete the data selected
mysqli_query($connection,"DELETE FROM posts WHERE sender='$sender' and Date='$time' ");
//jump back to profile page
header("location:profile1.php");
?>