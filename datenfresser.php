<?php
echo "<h3>Datenfresser</h3>";

$dbh = new PDO('sqlite:/var/datenfresser/datenfresser.db');

print "<table bgcolor=lightgrey>";


$data = $dbh->query("SELECT * FROM dataContainer");

foreach ($data->fetchAll(PDO::FETCH_ASSOC)
 as $row) {
	
	print "<tr>";
      	foreach($row as $value){
		print "<td>".$value."</td>";		
	}
	print "</tr>";
}

print "</table>";
?>
