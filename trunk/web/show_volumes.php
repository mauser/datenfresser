<?php

include("datenfresser_core.php");

$core = new datenfresser(); 
$core->print_header();

?>
<br />
<table>
	<tr><form method="post" action="show_volumes.php"><td>Add Volume:</td><td><input type="text" name="new_volume"></td><td><input type="submit" value="Add"></td></form></tr>
</table>
<br />	

<?

if(isset($_POST['new_volume']) and $_POST['new_volume'] != ""){
	$core->add_volume( $_POST['new_volume'] );
}

$dbh = new PDO('sqlite:/var/datenfresser/datenfresser.db');
$data = $dbh->query("SELECT * from 'volumes'");
$d = $data->fetchAll(PDO::FETCH_ASSOC);
foreach ($d as $row) {
	print "<table>\n";
	foreach( $row as $key => $value ){
		print "<tr><td>$key:</td><td>".$value."</td>";
	}
	print "</table><br />";		

}	



?>
