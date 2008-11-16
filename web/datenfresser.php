<?
	include("datenfresser_core.php");








$d = new datenfresser();
$d->print_header();

$dbh = new PDO('sqlite:/var/datenfresser/datenfresser.db');

print "<br /><table bgcolor=lightgrey>\n";
print "<tr><th>Name</th><th>Remote location</th><th>Comment</th></tr>";

$data = $dbh->query("SELECT name,remotePath,comment FROM dataContainer");

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
