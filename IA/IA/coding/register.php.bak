<?php
function isEmail($email){//check the format of the email address
   		$mode = '/\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*/';
   		if(preg_match($mode,$email)){	
  			return true;
 		}
  		else{
 			return false;
		}
 	}

 if (isset($_REQUEST['authcode'])) {//to check whether the input verification code is correct
        session_start();
        if (! (strtolower($_REQUEST['authcode'])==$_SESSION['authcode'])) //to compare the input value and the value of verification code
        {
			echo "<script>alert('Wrong Verification Code！');history.back(-1);</script>";
            exit();
        }
    }
include "testphpdb.php";
$user = $password = $contact="";
if (isset($_POST["submit"])) {
    if (empty($_POST["user"])) {//check whether the username inputted is empty
	 echo "<script>alert('User name cannot be empty');history.back(-1);</script>";//remind the user that username can not be empty
	 exit();
	} else {
        $user = $_POST["user"];
    }
	if (!isEmail($_POST["contact"])){//check whether the email address inputted is in valid format
		echo "<script>alert('Invalid email address');history.back(-1);</script>";//remind the user that email address is invalid
		exit();
	}else{
	$contact = $_POST["contact"];
	}
    if (empty($_POST["password"]) or empty($_POST["repassword"])) {//check whether the password or repassword inputted is empty
	echo "<script>alert('Password cannot be empty');history.back(-1);</script>";//remind the user that password can not be empty
       exit(); 

    }else if ($_POST["password"] != $_POST["repassword"])//check whether the password and repassword inputted is the same
    {
		echo "<script>alert('Inconsistent password');history.back(-1);</script>";//remind the user that passwords inputted are not the same
    exit(); 
    }  else {
        $password = $_POST["password"];
        $repassword = $_POST["repassword"];
    }

    $sql = "select * from userinfo where name = \"$user\"";
    $result = mysqli_query($connection, $sql);

    if (mysqli_num_rows($result) > 0) {
        echo "<script>alert('Username already be taken');history.back(-1);</script>";//check whether the username is already taken
    } else {
		$password = password_hash($password, PASSWORD_DEFAULT);//hash the password with salt
        $sql = "insert into userinfo(name,password,Contact) VALUES(\"$user\",\"$password\",\"$contact\")";//insert the data in the database
        
        $result1 = mysqli_query($connection, $sql);
        if ($result1) {	
            echo "<script>alert('Successful!');location.href='login.html';</script>";//jump to the log in page
        } else {
            echo "<script>alert('Database error!')</script>";//if not successfully insert the data in the database
        }
    }
}
?>


