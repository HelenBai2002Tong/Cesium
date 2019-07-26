<?php
session_start();
$_SESSION['username']='';//set the session as empty to log out
echo "<script>alert('Successfully log out!');location.href='login.html';</script>";// jump to the log in page
?>