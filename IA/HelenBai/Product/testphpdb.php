<?php
    
    $connection=mysqli_connect('localhost','Cats','password','catdb');//connect the PHP to the database(catdb)
    if(!$connection){
       exit('<h1>Fail to connect with database</h2>');//if cannot connect with the database, remind th user
}
 
//build up the inquiring
     mysqli_set_charset($connection, 'utf8');

?>