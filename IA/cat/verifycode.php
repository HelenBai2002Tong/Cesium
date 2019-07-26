<?php
//reference of online resource
    session_start();//to start session
   $image=imagecreatetruecolor(100, 30);//imagecreatetruecolor function: to make a picture   
   $bgcolor=imagecolorallocate($image, 255, 255, 255);//to make white background
   $textcolor=imagecolorallocate($image,0,0,255);//to make blue text
   imagefill($image, 0, 0, $bgcolor);
   $captch_code="";

   //to generate verification code
   for($i=0;$i<4;$i++){
     $fontsize=6;
     $x=($i*25)+rand(5,10);
     $y=rand(5,10);//for random position
    $data='abcdefghijkmnpqrstuvwxyz3456789';
    $fontcontent=substr($data,rand(0,strlen($data)-1),1);//strlen is a counter for the verification code

 $fontcolor=imagecolorallocate($image,rand(0,100),rand(0,100),rand(0,100));//random rgb

    imagestring($image,$fontsize,$x,$y,$fontcontent,$fontcolor); //draw a string horizontally
    $captch_code.=$fontcontent;
}
    $_SESSION['authcode']=$captch_code;//to save the variable as session variable

    
    //to make interferential points
    for($m=0;$m<=600;$m++){

     $x2=rand(1,99);
     $y2=rand(1,99);
     $pointcolor=imagecolorallocate($image,rand(0,255),rand(0,255),rand(0,255));
    imagesetpixel($image,$x2,$y2,$pointcolor);// draw several points horizontally
    }

    //to make interferential lines
   for ($i=0;$i<=10;$i++){
       $x1=rand(0,99);
       $y1=rand(0,99);
       $x2=rand(0,99);
       $y2=rand(0,99);
       $linecolor=imagecolorallocate($image,rand(0,255),rand(0,255),rand(0,255));
       imageline($image,$x1,$y1,$x2,$y2,$linecolor);//draw a line
   
   }
   header('content-type:image/png');
   imagepng($image);
   //to destroy
   imagedestroy($image);
?>

