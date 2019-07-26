<?php
session_start();
if(!isset($_POST['submit'])){//whether the button submit is clicked
    exit('Illegal');
}
include('testphpdb.php');
$username=$_POST['username'];//get the username from the html page
$password=$_POST['password'];//get the password from the html page

if ($username&&$password){//test whether the both username and password is inputted
    
	$sql="select * from userinfo where name='$username' ";
	$resultpwd = $connection->query($sql);
	$pwd = mysqli_fetch_array($resultpwd);
    $passvery = password_verify($password, $pwd['password']);//password verification
	if ($passvery){
		$_SESSION['username']=$username;// set a session for the username for further use
		header("refresh:0;url=mainviewing.php");// jumping to the mainviewing page
		exit;
	}else{
		echo "<script>alert('wrong username or password');history.back(-1);</script>";//if password is wrong
	}
}else{
	echo "<script>alert('name and password cannot be empty');hi	story.back(-1);</script>";// check if empty
}

					
?>