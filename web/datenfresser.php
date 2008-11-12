<html>
	<head>
		<title>Datenfresser</title>
		<link rel="stylesheet" type="text/css" href="datenfresser.css">

	</head>
	
	<body>
<div id="banner">
<?php
echo "<h3>Datenfresser</h3><a href='add_container.php'>Add container</a></div>";

$dbh = new PDO('sqlite:/var/datenfresser/datenfresser.db');

print "<br /><table bgcolor=lightgrey>";


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

	</body>
</html>
