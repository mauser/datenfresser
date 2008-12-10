<?
	include("datenfresser_core.php");


$d = new datenfresser();
$d->print_header();

$dbh = new PDO('sqlite:/var/datenfresser/datenfresser.db');

if($dbh){
	$d->print_error_message("Database error");
	exit;
}



print "<br /><br /><br /><br /><br />";

print "<table><tr><th>Running Jobs</th></tr>";

foreach($d->get_running_jobs() as $job){
	print "<tr><td>Job \"" . $job["name"] . "\" is running since  " . date(DATE_RFC822 ,  $job["start_timestamp"] ) . "</td></tr>";
}

print "</table><br>";

print "<table><tr><th>Name</th><th>Remote location</th><th>Comment</th></tr>";

$data = $dbh->query("SELECT dataID,name,remotePath,comment FROM dataContainer");



foreach ($data->fetchAll(PDO::FETCH_ASSOC)
 as $row) {
	
	print "<tr>";
		print "<td>".$row['name']."</td>";
		print "<td>".$row['remotePath']."</td>";
		print "<td>".$row['comment']."</td>";
		print "<td><a href='show_container.php?id=".$row['dataID']."'><img src='images/status.png' width='20' height='20' border='0'></a>";
		print "<a href='show_logs.php?id=".$row['dataID']."'><img src='images/history.png' width='20' height='20' border='0'></a>";
		print "<a href='delete_container.php?id=".$row['dataID']."'><img src='images/warning.png' width='20' height='20' border='0'></a></td>";
		
	print "</tr>";
}

print "</table>";
?>

	</body>
</html>
