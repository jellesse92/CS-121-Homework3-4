<?php
/*
CS 121 - Information Retreival
  Authors : Aisha
            Jasmine
            Helio

  Date    : 01 June 2017

Web interface for our search engine.
*/

// SQL TEST
/*
$servername = "localhost";
$username = "root";
$password = "test";
$dbname = "cs121";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) {
  echo "Something went wrong" . "<hr>";
    die("Connection failed: " . $conn->connect_error);
}

$sql = "SELECT docid, url FROM bookkeeping LIMIT 10";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    // output data of each row
    while($row = $result->fetch_assoc()) {
        echo "docid: " . $row["docid"]. " - URL: " . $row["url"]. "<br>";
    }
} else {
    echo "0 results";
}
$conn->close();

echo "<hr>";
*/

if (!empty($_GET['term'])){
  $SearchTerm = $_GET['term'];
  $term_params = "";
  foreach($SearchTerm as $thisTerm){
    $term_params .= $thisTerm . " ";
  }
  //echo $term_params;
  $outarray = array();
  exec("python pytest.py " . $term_params, $outarray);
} else{
  $term_params = '';
}

//print_r($outarray);

function get_title($url){
  $str = file_get_contents($url);
  if(strlen($str)>0){
    $str = trim(preg_replace('/\s+/', ' ', $str)); // supports line breaks inside <title>
    preg_match("/\<title\>(.*)\<\/title\>/i",$str,$title); // ignore case
    return $title[1];
  } else{
    return "Title Not Found :(";
  }
}

function curl_get_contents($url)
{
    $ch = curl_init();

    curl_setopt($ch, CURLOPT_HEADER, 0);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_URL, $url);

    $data = curl_exec($ch);
    curl_close($ch);

    return $data;
}
?>

<!DOCTYPE html>
<html>

<head>
  <title>CS121 SE</title>
  <!-- Latest compiled and minified CSS -->
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">

<!-- Optional theme -->
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap-theme.min.css" integrity="sha384-rHyoN1iRsVXV4nD0JutlnGaslCJuC7uwjduW9SVrLvRYooPp2bWYgmgJQIXwl/Sp" crossorigin="anonymous">

<!-- Latest compiled and minified JavaScript -->
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>
</head>

<body>
  <div class="row">
    <div class="col-md-3">
    </div>
    <div class="col-md-5">
      <h1>
        Discussion 4 Group 18 SE
      </h1>
    </div>
    <div class="col-md-4">
    </div>
  </div>
  <div class="row">
    <div class="col-md-3">
    </div>
    <div class="col-md-5">
        <span style="width: 80%">
          <input style="width: inherit" type="text" id="search-term" value="<?=$term_params?>">
        </span>
        <span>
          <input type="button" value="Search" onclick="executeQuery()">
        </span>
    </div>
    <div class="col-md-4">
    </div>
  </div>
  <br />
  <br />
  <br />
  <?php
  if (!empty($SearchTerm)){
    foreach($outarray as $content){
      //echo $content;
      //echo "<hr>";
      $contentInfo = explode(",X,", $content);
      //print_r($contentInfo);
      //echo "<hr>";
      $score = $contentInfo[0];
      $document = $contentInfo[1];
      $url = "http://" . $contentInfo[2];
      //echo $score;
      //echo "<hr>";
      //echo $document;
      //echo "<hr>";
      //echo $url;
      //echo "<hr>";
      $title = get_title($url);
      //echo $title . "<hr>";
  ?>
  <div class="row">
    <div class="row">
      <div class="col-sm-12">
        <h3 style="margin-left: 20px">
          <a href="<?=$url?>"><?=$title?></a>
        </h3>
      </div>
    </div>

    <div class="row">
      <div class="col-sm-12">
        <p style="font-size: 6px; margin-left: 20px">
          <?=$url?>
        </p>
      </div>
    </div>

    <div class="row">
      <div class="col-sm-12">
        <span style="margin-left: 20px">
          <b>Document ID:</b> <?=$document?>,
        </span>
        <span>
          <b>Score:</b> <?=$score?>
        </span>
      </div>
    </div>
  </div>
  <?php
    }
  }
  ?>

  <script>
    function executeQuery(){
      var terms = document.getElementById("search-term").value;
      console.log(terms);
      var term_array = terms.split(" ");
      term_str = "";
      for (i = 0; i < term_array.length; i++){
        term_str = term_str + "term[]=" + term_array[i] + "&";
      }
      console.log(term_str);
      window.location = "index.php?" + term_str.substr(0, term_str.length - 1);
    }
  </script>
</body>

</html>
