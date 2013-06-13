<?php
$FAR = 2500;
$opts['hn'] = 'localhost';
$opts['un'] = 'your_user_name_here';
$opts['pw'] = 'your_password';
$opts['db'] = 'your_database_name';
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
if (isset($_GET["dtm"])) $dtm = preg_replace('/[^0-9.\-]/', '', $_GET["dtm"]); else $dtm = "";
if (isset($_GET["x"])) $x = preg_replace('/[^0-9.\-]/', '', $_GET["x"]); else $x = "";
if (isset($_GET["z"])) $z = preg_replace('/[^0-9.\-]/', '', $_GET["z"]); else $z = "";
if (isset($_GET["json"])) $json = preg_replace('/[^0-9a-f:.\-\"TrueFals\[\],:]/', '', $_GET["json"]); else $json = "";
if ($id == "" || $dtm == "" || $x == "" || $z == "" || $json == "") {
  echo "error";
 } else {
  // delete old records
  $q = "DELETE FROM rpi_json WHERE tm < (CURRENT_TIMESTAMP - INTERVAL 1 HOUR)";
  $res = mysql_query($q, $dbh);
  // insert this record
  $tm_now = microtime(true);
  $rel_tm = $tm_now - $dtm;
  $pos = strpos($json, ",");
  $json = substr($json, 0, $pos) . "," . $rel_tm . substr($json, $pos);
  $q = "SELECT id FROM rpi_json WHERE id='" . $id ."'";
  $res = mysql_query($q, $dbh);
  if ($res && mysql_num_rows($res) > 0) {
    $q = "UPDATE rpi_json SET x=" . $x . ", z=" . $z . ", tm=CURRENT_TIMESTAMP, json='" . $json . "' WHERE id='" . $id . "'";
    $res = mysql_query($q, $dbh);
  } else {
    $q = "INSERT INTO rpi_json (id, x, z, tm, json) VALUES ('" . $id . "', " . $x . ", " . $z . ", CURRENT_TIMESTAMP, '" . $json . "') ";
    $res = mysql_query($q, $dbh);
  }

  // return json list
  $q = "SELECT json FROM rpi_json WHERE NOT (id = '" . $id . "') AND 
           x > " . ($x - $FAR) . " AND x < " . ($x + $FAR) . " AND z > " . ($z - $FAR) . " AND z < " . ($z + $FAR);
  $res = mysql_query($q, $dbh);
  if ($res) {
    $n =  mysql_num_rows($res);
    echo "[" . $tm_now . ",";
    for ($i=0; $i<$n; $i++) {
        $row = mysql_fetch_object($res);
        echo (($i > 0) ? "," : "") . $row->json;
    }
    echo "]";
  }
  else  echo "sql error";
}
?>
