<?php
session_start();// start the session
date_default_timezone_set("Asia/Shanghai");
//retrieve from online resource of API for the recognition and translation
include('testphpdb.php');
/**
 * @param string $url
 * @param string $param
 * @return - http response body if succeeds, else false.
 */

function request_post($url = '', $param = '')
{
    if (empty($url) || empty($param)) {
        return false;
    }

    $postUrl = $url;
    $curlPost = $param;
    $curl = curl_init();
    curl_setopt($curl, CURLOPT_URL, $postUrl);
    curl_setopt($curl, CURLOPT_HEADER, 0);
    curl_setopt($curl, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($curl, CURLOPT_POST, 1);
    curl_setopt($curl, CURLOPT_POSTFIELDS, $curlPost);
    curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, FALSE);
    curl_setopt($curl, CURLOPT_SSL_VERIFYHOST, FALSE);
    curl_setopt($curl, CURLOPT_SSLVERSION, 1);

    $data = curl_exec($curl);//run curl
    curl_close($curl);

    return $data;
}

$url = 'https://aip.baidubce.com/oauth/2.0/token';
$post_data['grant_type'] = 'client_credentials';
$post_data['client_id'] = '9ENKdjW87aPEUnkzli0eOdkD';
$post_data['client_secret'] = 'ZR3UjOSAMKBXzoRwNdpfuOFvaQVjqA6B';
$res = request_post($url, $post_data);
$index = (strripos($res, '"access_token":"') + 16);
$token = (string)(substr($res, $index, 70));


//translation
define("CURL_TIMEOUT", 2000);
define("URL", "http://openapi.youdao.com/api");
define("APP_KEY", "3d1cb434c224a95e"); // my application ID
define("SEC_KEY", "o0eW1THOhc3v9hqJjjPUiZZZREYPJsA5"); // my key

function do_request($q)
{
    $salt = create_guid();
    $args = array(
        'q' => $q,
        'appKey' => APP_KEY,
        'salt' => $salt,
    );
    $args['from'] = 'zh-CHS';
    $args['to'] = 'EN';
    $args['signType'] = 'v3';
    $curtime = strtotime("now");
    $args['curtime'] = $curtime;
    $signStr = APP_KEY . truncate($q) . $salt . $curtime . SEC_KEY;
    $args['sign'] = hash("sha256", $signStr);
    $ret = call(URL, $args);
    return $ret;
}

// send a request
function call($url, $args = null, $method = "post", $testflag = 0, $timeout = CURL_TIMEOUT, $headers = array())
{
    $ret = false;
    $i = 0;
    while ($ret === false) {
        if ($i > 1)
            break;
        if ($i > 0) {
            sleep(1);
        }
        $ret = callOnce($url, $args, $method, false, $timeout, $headers);
        $i++;
    }
    return $ret;
}

function callOnce($url, $args = null, $method = "post", $withCookie = false, $timeout = CURL_TIMEOUT, $headers = array())
{
    $ch = curl_init();
    if ($method == "post") {
        $data = convert($args);
        curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
        curl_setopt($ch, CURLOPT_POST, 1);
    } else {
        $data = convert($args);
        if ($data) {
            if (stripos($url, "?") > 0) {
                $url .= "&$data";
            } else {
                $url .= "?$data";
            }
        }
    }
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_TIMEOUT, $timeout);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    if (!empty($headers)) {
        curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
    }
    if ($withCookie) {
        curl_setopt($ch, CURLOPT_COOKIEJAR, $_COOKIE);
    }
    $r = curl_exec($ch);
    curl_close($ch);
    return $r;
}

function convert(&$args)
{
    $data = '';
    if (is_array($args)) {
        foreach ($args as $key => $val) {
            if (is_array($val)) {
                foreach ($val as $k => $v) {
                    $data .= $key . '[' . $k . ']=' . rawurlencode($v) . '&';
                }
            } else {
                $data .= "$key=" . rawurlencode($val) . "&";
            }
        }
        return trim($data, "&");
    }
    return $args;
}

// uuid generator
function create_guid()
{
    $microTime = microtime();
    list($a_dec, $a_sec) = explode(" ", $microTime);
    $dec_hex = dechex($a_dec * 1000000);
    $sec_hex = dechex($a_sec);
    ensure_length($dec_hex, 5);
    ensure_length($sec_hex, 6);
    $guid = "";
    $guid .= $dec_hex;
    $guid .= create_guid_section(3);
    $guid .= '-';
    $guid .= create_guid_section(4);
    $guid .= '-';
    $guid .= create_guid_section(4);
    $guid .= '-';
    $guid .= create_guid_section(4);
    $guid .= '-';
    $guid .= $sec_hex;
    $guid .= create_guid_section(6);
    return $guid;
}

function create_guid_section($characters)
{
    $return = "";
    for ($i = 0; $i < $characters; $i++) {
        $return .= dechex(mt_rand(0, 15));
    }
    return $return;
}

function truncate($q)
{
    $len = strlen($q);
    return $len <= 20 ? $q : (substr($q, 0, 10) . $len . substr($q, $len - 10, $len));
}

function ensure_length(&$string, $length)
{
    $strlen = strlen($string);
    if ($strlen < $length) {
        $string = str_pad($string, $length, "0");
    } else if ($strlen > $length) {
        $string = substr($string, 0, $length);
    }
}

$title = $description = '';
if (empty($_SESSION['username'])) {//check whether the user is logged in 
    echo "<script>alert('please log in');parent.location.href='layout1.html';</script>";
} else {
    $username = $_SESSION['username'];//get the username from session
    $title = $_POST['title'];
    $description = $_POST['description'];
    $path = "figure/";//set the path of the storage of the file
    if (!file_exists($path)) {
        mkdir($path, 0777);
    }
    if (empty($title)) {//check whether the title is empty
        echo "<script>alert('Title cannot be empty');history.back(-1);</script>";
    } else {

        if ((empty($_FILES['file']['tmp_name'])) || ($_FILES["file"]["error"] > 0)) {
            echo "<script>alert('please upload valid files');history.back(-1);</script>";
        } else {
            $allowedExts = array("gif", "jpeg", "jpg", "png");
            $temp = explode(".", $_FILES["file"]["name"]);
            $extension = end($temp);
            if ((($_FILES["file"]["type"] == "image/gif")
                    || ($_FILES["file"]["type"] == "image/jpeg")
                    || ($_FILES["file"]["type"] == "image/jpg")
                    || ($_FILES["file"]["type"] == "image/pjpeg")
                    || ($_FILES["file"]["type"] == "image/x-png")
                    || ($_FILES["file"]["type"] == "image/png"))
                && ($_FILES["file"]["size"] < 2048000)//check the size of the file & whether the file is an image
                && in_array($extension, $allowedExts)) {

                $filename = uniqid($username) . "." . $extension;//rename the file to ensure there is no same name
                $Name = $path . $filename;
                $try = move_uploaded_file($_FILES["file"]["tmp_name"], $Name);//store the image
				//the api to do cat face recognition
                if ($try == true) {
                    $url = 'https://aip.baidubce.com/rest/2.0/image-classify/v1/animal?access_token=' . $token;
                    $img = file_get_contents($Name);
                    $img = base64_encode($img);
                    $bodys = array(
                        'image' => $img,
                        'top_num' => 6
                    );
                    $res = request_post($url, $bodys);
                    $index1 = (strpos($res, '"name":') + 9);
                    $index2 = strpos($res, '}');
                    $length = ($index2 - $index1 - 1);
                    $species = (string)(substr($res, ($index1), (($length))));
                    // to translate
                    $q = $species;
                    $ret = do_request($q);
                    $ret = json_decode($ret, true);
                    $A = $ret['translation'][0];//get the breed of the cat
                    if ($A == 'The animals') {//check whether the file contains a cat
                        echo "<script>alert('please only upload picture with cats in it');history.back(-1);</script>";
                    } else {
						$date = date("Y-m-d h:i:sa");//get the date
						//insert the information from the posts to the database. including the username, title, description, store path of the image,
						//breed of cat and the date&time
                        $sql = "INSERT INTO posts(sender,title,description,image,Type,Date) 
						VALUES(\"$username\",\"$title\",\"$description\",\"$Name\",\"$A\",\"$date\")";
                        $result1 = mysqli_query($connection, $sql);
                        if (!$result1) {
                            echo "<script>alert('Database error!')</script>";//if can not insert the data into database, remind the user
                        } else {
                            echo "<script>alert('Successful post!');parent.location.href='mainviewing.php';</script>";//if successful post, remind the user and jump to mainviewing page
                        }
                    }
                } else {
                    echo "<script>alert('Failed to upload the picture!');</script>";//if can not move the image to the storage path, remind the user
                }
            } else {
                echo "<script>alert('please only upload gif/jpeg/jpg/png files');history.back(-1);</script>";//if the file is not an image, remind the user
            }
        }
    }
}


?>
