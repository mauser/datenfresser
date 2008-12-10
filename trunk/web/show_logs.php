<?php

include("datenfresser_core.php");

$core = new datenfresser(); 
$core->print_header();

if($_GET["id"] != ""){



$dbh = new PDO('sqlite:/var/datenfresser/datenfresser.db');

print "<br /><table>\n";

print "<tr><th>Type</th><th>Start</th><th>End</th><th>Status</th></tr>";


$data = $dbh->query("SELECT * FROM log WHERE dataID ='".$_GET["id"]."' ORDER BY start_timestamp desc");
$d = $data->fetchAll(PDO::FETCH_ASSOC);

$date_string = "F j, Y, H:i ";

foreach ($d as $row) {
	
	print "<tr>";
	#print "<td>". $row['logID'].  "</td>";
	#print "<td>". $row['dataID'].  "</td>";
	print "<td>". $row['type'].  "</td>";
	print "<td>". @date($date_string , $row['start_timestamp']).  "</td>";
	print "<td>". @date($date_string , $row['end_timestamp']).  "</td>";
	print "<td>". $row['status'].  "</td>";

	/*foreach( $row as $key => $value ){
		print "<td>$key:</td><td>".$value."</td>";
	}*/	
	print "</tr>";
}

	
}

?>
