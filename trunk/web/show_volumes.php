<?php

include("datenfresser_core.php");

$core = new datenfresser(); 
$core->print_header();


$dbh = new PDO('sqlite:/var/datenfresser/datenfresser.db');
print "<br /><table>\n";
$data = $dbh->query("SELECT * from 'volumes'");
$d = $data->fetchAll(PDO::FETCH_ASSOC);
foreach ($d as $row) {
	foreach( $row as $key => $value ){
		print "<tr><td>$key:</td><td>".$value."</td>";
	}	
}	



?>
