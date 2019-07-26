<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Profile</title>
    <style>
	ul
{
list-style-type:none;
margin:0;
padding:0;
padding-top:6px;
padding-bottom:6px;
}
li
{
display:inline;
}

#title
{
width:200px;
height:20px;
}
#description
{
width:400px;
height:100px;
}

div
{
position: absolute;
top: 25%;
left: 35%;
}

	
</style>
</head>
<body>
<br>
<br>
<center>
<h2>FatCats</h2>

<ul>
<li><a href="mainviewing.php" style= 'font-weight:bold;color:#FFFFFF; background-color:#bebebe;text-align:center;padding:6px;
text-decoration:none; text-transform:uppercase' onMouseOver="this.style.backgroundColor='#cc0000';" 
onMouseOut="this.style.backgroundColor='#bebebe';">Moments</a></li><!-- jump to the mainviewing page -->
<li><a href="post.html"style= 'font-weight:bold;color:#FFFFFF; background-color:#bebebe;text-align:center;padding:6px;
text-decoration:none; text-transform:uppercase'onMouseOver="this.style.backgroundColor='#cc0000';" 
onMouseOut="this.style.backgroundColor='#bebebe';">Post a new message</a></li><!-- jump to the post page -->
<li><a href="profile1.php"style= 'font-weight:bold;color:#FFFFFF; background-color:#bebebe;text-align:center;padding:6px;
text-decoration:none; text-transform:uppercase'onMouseOver="this.style.backgroundColor='#cc0000';" 
onMouseOut="this.style.backgroundColor='#bebebe';">Profile</a></li><!-- jump to the profile page -->
<li><a href="logout.php"style= 'font-weight:bold;color:#FFFFFF; background-color:#bebebe;text-align:center;padding:6px;
text-decoration:none; text-transform:uppercase'onMouseOver="this.style.backgroundColor='#cc0000';" 
onMouseOut="this.style.backgroundColor='#bebebe';">LOG OUT</a></li><!-- click to log out -->
</ul>
</center>



<form action="profile.php" method="post">
    <div>
        <h2>UPDATE Profile</h2>
	   Email Address(e.g. example@cat.com)<br><!-- input space to change email address-->
		<label for="contact"></label><input id="contact" name="contact" type="text" ><br>
		<br><!--button for submit the change-->
        <button type="submit" name="submit" >Save Changes</button>
     
</form>

<br>
<h2> My Posts</h2>
	
<!-- a table for all posts from the current user-->
<table border= '1' width='570' style="word-break: keep-all;  word-wrap:break-word;">

<tr><th>Title</th><th>Description</th><th>Post Time</th><th>Operation</th></tr>

<?php
session_start();
if (empty($_SESSION['username'])) {
    echo "<script>alert('please log in');parent.location.href='layout1.html';</script>";//check if logged in, if not jump to the layout page
}
$username=$_SESSION['username'];//get the current username
include('testphpdb.php');
$result = mysqli_query($connection, "select * from posts WHERE sender = '$username' ORDER BY Date DESC;");//get all the posts from the user from the database

if (mysqli_num_rows($result) > 0) {
while($row = mysqli_fetch_assoc($result)) {//show the result one by one
		echo "<tr><td class='td' width='100'>".$row["title"]."</td><td class='td' width='300'>".$row["description"]."</td><td class='td' width='120'>"
		.$row["Date"]."</td><td class='td' width='100'><a href='del.php?date=$row[Date]'>Remove</a><br><a href='edit.php?title=$row[title]&description
		=$row[description]&date=$row[Date]'>Edit</a></td></tr>";
    }
}else{
	echo " ";
}

?>

</table>
</div>

</body>
</html>
