<?php
include("testphpdb.php");//connect the database
$result = mysqli_query($connection,"select Type from posts ORDER BY Type DESC;" );//retrieve all breed of cat from the database
$alltype=array();//set a new array for all breed of the cat
if (mysqli_num_rows($result) > 0) {
    while($row = mysqli_fetch_assoc($result)) {
		if (!in_array($row['Type'],$alltype)){//check whether the type is already in the array
			array_push($alltype,$row['Type']);
		}
	}
}else{
	$alltype=array();
}
?>