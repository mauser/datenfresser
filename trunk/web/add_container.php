<?php

include("datenfresser_core.php");

$core = new datenfresser(); 
$core->print_header();

if($_POST["name"] != ""){
	
	$name = $_POST['name'];
	$rpath = $_POST['rpath'];
	$comment = $_POST['comment'];
	$options = $_POST['options'];
	$schedule = $_POST['schedule'];
	$archive = $_POST['archive'];
	$archive_ttl = $_POST['archive_ttl'];
	$compress = $_POST['compress'];
	$group = "ALL";
	$type = "rsync";

	#$core->init();
	$core->addContainer( $name, $comment, $rpath, $type, $options, $schedule, $group,$archive,$compress,$archive_ttl);
}

?>


<h3>Create new container</h3>
<form action="add_container.php" method="post">
<table>
	<tr><td>Name:</td><td><input type="text" name="name"></td></tr>
	<tr><td>Remote path:</td><td><input type="text" name="rpath"></td></tr>
	<tr><td>Rsync options:</td><td><input type="text" name="options"></td></tr>
	<tr><td>Comment:</td><td><input type="text" name="comment"></td></tr>
	<tr><td>Schedule:</td><td>
					<select name="schedule">
						<option>daily</option>
						<option>weekly</option>
						<option>monthly</option>
					</select>
				</td></tr>
	
	<tr><td>Archive:</td><td>
					<select name="archive">
						<option>disabled</option>
						<option>daily</option>
						<option>weekly</option>
						<option>monthly</option>
					</select>
				</td></tr>
	<tr><td>Compress:</td><td><input type="checkbox" name="compress"></td></tr>
	<tr><td>Keep archives:</td><td><input type="text" name="archive_ttl"> days</td></tr>


	<tr><td colspan="2"><input type="submit"></td></tr>
</table>
</form>
