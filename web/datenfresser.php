<?
	include("datenfresser_core.php");








$d = new datenfresser();
$d->print_header();

$dbh = new PDO('sqlite:/var/datenfresser/datenfresser.db');

print "<br /><table bgcolor=lightgrey>\n";
print "<tr><th>Nr.</th><th>Name</th><th>Locale location</th><th>Remote location</th><th>Comment</th><th>Type</th><th>Options</th><th>Schedule</th><th>Group</th></tr>";

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
