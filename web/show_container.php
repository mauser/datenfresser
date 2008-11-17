<?php

include("datenfresser_core.php");

$core = new datenfresser(); 
$core->print_header();

if($_GET["id"] != ""){



$dbh = new PDO('sqlite:/var/datenfresser/datenfresser.db');

print "<br /><table bgcolor=lightgrey>\n";

$data = $dbh->query("SELECT dataID,name,remotePath,comment,schedule,options FROM dataContainer WHERE dataID ='".$_GET["id"]."'");
$d = $data->fetchAll(PDO::FETCH_ASSOC);
foreach ($d as $row) {

	foreach( $row as $key => $value ){
		print "<tr><td>$key:</td><td>".$value."</td>";
	}	
}

	
}

?>
