<?
	include("datenfresser_core.php");


$d = new datenfresser();
$d->print_header();

$dbh = new PDO('sqlite:/var/datenfresser/datenfresser.db');

print "<br /><table bgcolor=lightgrey>\n";
print "<tr><th>Name</th><th>Remote location</th><th>Comment</th></tr>";

$data = $dbh->query("SELECT dataID,name,remotePath,comment FROM dataContainer");

foreach ($data->fetchAll(PDO::FETCH_ASSOC)
 as $row) {
	
	print "<tr>";
		print "<td>".$row['name']."</td>";
		print "<td>".$row['remotePath']."</td>";
		print "<td>".$row['comment']."</td>";
		print "<td><a href='delete_container.php?id=".$row['dataID']."'>delete</a></td>";
		
	print "</tr>";
}

print "</table>";
?>

	</body>
</html>
