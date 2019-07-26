<?php
function isEmail($email){
   		$mode = '/\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*/';
   		if(preg_match($mode,$email)){
  			return true;
 		}
  		else{
 			return false;
		}
 	}

 if (isset($_REQUEST['authcode'])) {
        session_start();
        if (! (strtolower($_REQUEST['authcode'])==$_SESSION['authcode'])) //to compare the input value and the value of verification code
        {
			echo "<script>alert('Wrong Verification Code！');history.back(-1);</script>";
            exit();
        }
    }
include "testphpdb.php";
$user = $password = $contact="";
$userErr = $passwordErr = $repasswordErr = $conErr="";
if (isset($_POST["submit"])) {
    if (empty($_POST["user"])) {
	 echo "<script>alert('User name cannot be empty');history.back(-1);</script>";
	 exit();
	} else {
        $user = $_POST["user"];
    }
	if (!isEmail($_POST["contact"])){
		echo "<script>alert('Invalid email address');history.back(-1);</script>";
		exit();
	}else{
	$contact = $_POST["contact"];
	}
    if (empty($_POST["password"]) or empty($_POST["repassword"])) {
	echo "<script>alert('Password cannot be empty');history.back(-1);</script>";
       exit(); 

    }else if ($_POST["password"] != $_POST["repassword"])
    {
		echo "<script>alert('Inconsistent password');history.back(-1);</script>";
    exit(); 
    }  else {
        $password = $_POST["password"];
        $repassword = $_POST["repassword"];
        echo "<br>";
    }

    $sql = "select * from userinfo where name = \"$user\"";
    $result = mysqli_query($connection, $sql);

    if (mysqli_num_rows($result) > 0) {
        echo "<script>alert('Username already be taken');history.back(-1);</script>";
    } else {
		$password = password_hash($password, PASSWORD_DEFAULT);
        $sql = "insert into userinfo(name,password,Contact) VALUES(\"$user\",\"$password\",\"$contact\")";
        
        $result1 = mysqli_query($connection, $sql);
        if ($result1) {	
            echo "<script>alert('Successful!');location.href='login.html';</script>";
        } else {
            echo "<script>alert('Database error!')</script>";
        }
    }
}
?>


