<?php
include('Type.php');//get the variable from type
?>
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

			
</style>
</head>
<body>
<center>
<div>
<h2>FatCats</h2>
<ul>
<li><a href="mainviewing.php">Moments</a></li><!-- jump to the mainviewing page -->
<li><a href="post.html">Post a new message</a></li><!-- jump to the post page -->
<li><a href="profile1.php">Profile</a></li><!-- jump to the profile page -->
<li><a href="logout.php">LOG OUT</a></li><!-- click to log out -->
</ul>

</div>
<form action='select.php' method='post'>
<br>
<b>The type of the cats you want:</b>
<?php
//generate a drop-down box of all types of cats
echo '<select id="type" name="type">';
foreach($alltype as $word){ 
  echo '<option value="'.$word.'">'.$word.'</option>'; 
} 
echo'</select>';
?>
<button> See About </button>
<hr></hr>
</form>
</body>
</html>

<?php
include('testphpdb.php');
// sort the output by time
$result = mysqli_query($connection,"select * from posts ORDER BY Date DESC;" );
// show the results in the database
if (mysqli_num_rows($result) > 0) {
    while($row = mysqli_fetch_assoc($result)) {
		$F=(string)$row["sender"];
		$E=mysqli_query($connection, "select * from userinfo WHERE name = '$F' ");
		$E=mysqli_fetch_assoc($E);
		$E=$E["Contact"];//get the contact info from the table userinfo 
        echo "<b>". "Sender: ". '</b>'. $row["sender"] . '<br>';
		echo "<b>". "Contact Information: ".'</b>' . $E . '<br>';
		echo wordwrap("<b>". "Title: " .'</b>'. $row["title"], 50, "<br>\n");//automatic linefeed
		echo "<br>";
		$mystr="<b>". "Description: ". '</b>'.$row["description"];
		echo wordwrap($mystr,50,"<br>\n");//automatic linefeed
		echo "<br>";
		echo "<b>". "Cat Type: ".'</b> '. $row["Type"]. '<br>';
		echo "<b>". "Date: " .'</b>'. $row["Date"] . '<br>' ;
		$IMGSC=$row['image'];		
		echo "<img widht=200 height=200 src = '$IMGSC' > <br>"; // show the image
		echo "<hr>";
    }
} else {
    echo " ";
}

?>
</center>