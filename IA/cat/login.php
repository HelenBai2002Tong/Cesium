<?php
session_start();
if(!isset($_POST['submit'])){
    exit('Illegal');
}
include('testphpdb.php');
$username=$_POST['username'];
$password=$_POST['password'];

if ($username&&$password){//test whether the password is correct
    
	$sql="select * from userinfo where name='$username' ";
	$resultpwd = $connection->query($sql);
	$pwd = mysqli_fetch_array($resultpwd);
    $passvery = password_verify($password, $pwd['password']);
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