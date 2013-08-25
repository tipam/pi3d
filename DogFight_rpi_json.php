<?php
/************************************************************************
 * script to run on server to store and serve information serialised in
 * json format for the pi3d demos/DogFight.py example
 * This file has been renamed to DogFight_rpi_json.php for clarity
 * when copied to the server it must have the same name used in the url
 * used in DogFight.py c. line 333
 * *********************************************************************/
$FAR = 5000;
$opts['hn'] = 'localhost';
$opts['un'] = 'your_db_username';
$opts['pw'] = 'your_db_password';
$opts['db'] = 'your_database';
//////////////////////////////////////////////////      connect to db
if ($dbh = mysql_pconnect($opts['hn'].':3306', $opts['un'], $opts['pw']))
{
  mysql_select_db($opts['db']);
}
else
{
  die('could not connect to MySQL');
}

if (isset($_GET["id"])) $id = preg_replace('/[^0-9a-f:]/', '', $_GET["id"]); else $id = "";
if (isset($_GET["tm"])) $tm = preg_replace('/[^0-9.\-]/', '', $_GET["tm"]); else $tm = "";
if (isset($_GET["x"])) $x = preg_replace('/[^0-9.\-]/', '', $_GET["x"]); else $x = "";
if (isset($_GET["z"])) $z = preg_replace('/[^0-9.\-]/', '', $_GET["z"]); else $z = "";
if (isset($_GET["json"])) $json = preg_replace('/[^0-9a-f:.,\-\"TrueFals\[\]]/', '', $_GET["json"]); else $json = "";
if (isset($_GET["damage"])) $damage = preg_replace('/[^0-9.\-]/', '', $_GET["damage"]); else $damage = "";
if (isset($_GET["nearest"])) $nearest = preg_replace('/[^0-9a-f:]/', '', $_GET["nearest"]); else $nearest = "";
if ($id == "" || $tm == "" || $x == "" || $z == "" || $json == "") {
  echo "error";
 } else {
  // delete old records
  $q = "DELETE FROM rpi_json WHERE tm < (CURRENT_TIMESTAMP - INTERVAL 1 HOUR)";
  $res = mysql_query($q, $dbh);
  // insert this record
  $tm_now = microtime(true);
  $rel_tm = $tm_now - $tm; //timing difference between pi and server
  $pos = strpos($json, ","); //insert in json string at location [1]
  $json = substr($json, 0, $pos) . "," . $rel_tm . substr($json, $pos);
  $q = "SELECT damage FROM rpi_json WHERE id='" . $id ."'";
  $res = mysql_query($q, $dbh);
  if ($res && mysql_num_rows($res) > 0) {
    $row = mysql_fetch_object($res);
    $own_damage = $row->damage;
    $q = "UPDATE rpi_json SET x=" . $x . ", z=" . $z . ", tm=CURRENT_TIMESTAMP, json='" . $json . "' WHERE id='" . $id . "'";
    $res = mysql_query($q, $dbh);
  } else {
    $own_damage = 0.0;
    $q = "INSERT INTO rpi_json (id, x, z, tm, json) VALUES ('" . $id . "', " . $x . ", " . $z . ", CURRENT_TIMESTAMP, '" . $json . "') ";
    $res = mysql_query($q, $dbh);
  }
  // update damage of nearest
  if ($nearest != "" && $damage != 0) {
    if ($damage < 0) $d_str = "0.0"; // negative damage used to reset to zero
    else $d_str = "damage + ".$damage;
    $q = "UPDATE rpi_json SET damage = " . $d_str . " WHERE id='" . $nearest . "'";
    $res = mysql_query($q, $dbh);
  }
  // return json list
  $q = "SELECT json FROM rpi_json WHERE NOT (id = '" . $id . "') AND 
           x > " . ($x - $FAR) . " AND x < " . ($x + $FAR) . " AND z > " . ($z - $FAR) . " AND z < " . ($z + $FAR);
  $res = mysql_query($q, $dbh);
  if ($res) {
    $n =  mysql_num_rows($res);
    if ($n > 0) {
      echo "[" . $rel_tm . "," . $own_damage . ",";
      for ($i=0; $i<$n; $i++) {
        $row = mysql_fetch_object($res);
        echo (($i > 0) ? "," : "") . $row->json;
      }
      echo "]";
    }
    else echo "nobody near" ;
  }
  else  echo "sql error";
}
?>
