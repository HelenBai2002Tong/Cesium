<?php
session_start();
$title=$_GET['title'];
$description=$_GET['description'];
$olddate=$_GET['date'];
$_SESSION['date']=$olddate;
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Posting</title>
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
a:link,a:visited
{
font-weight:bold;
color:#FFFFFF;
background-color:#bebebe;
text-align:center;
padding:6px;
text-decoration:none;	
text-transform:uppercase;
}
a:hover,a:active
{
background-color:#cc0000;
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
top: 5%;
left: 40%;
}
			
</style>
</head>
<body>
<div>
<h2>FatCats</h2>
<ul>
<li><a href="mainviewing.php">Moments</a></li>
<li><a href="post.html">Post a new message</a></li>
<li><a href="profile1.php">Profile</a></li>
<li><a href="logout.php">LOG OUT</a></li>
</ul>
<form action="update.php" method="post" enctype="multipart/form-data">
<h3>Edit</h3>
<p>
Title:<br>
<label for="title"></label>
<input id="title" name="title" type="text" value="<?php print_r($title)?>" /><br>
Description:(No more than 400 characters(including space))<br>
<input name="description" id="description" value="<?php print_r($description)?>" rows="5" cols="40"></input>
<br>

<button>POST</button>
</form>
</p>

</div>

</body>
</html>
