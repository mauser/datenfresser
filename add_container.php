<?php

if($_POST["name"] != ""){
	include("datenfresser_core.php");
	print "Name!!!";
	
	$name = $_POST['name'];
	$rpath = $_POST['rpath'];
	$comment = $_POST['comment'];
	$options = $_POST['options'];
	$schedule = $_POST['schedule'];
	$group = "ALL";
	$type = "rsync";

	$core = new datenfresser(); 
	#$core->init();
	$core->addContainer( $name, $comment, $path, $type, $options, $schedule, $group);
}

?>


<h3>Create new container</h3>
<form action="add_container.php" method="post">
<table>
	<tr><td>Name:</td><td><input type="text" name="name"></td></tr>
	<tr><td>Remote path:</td><td><input type="text" name="rpath"></td></tr>
	<tr><td>Rsync options:</td><td><input type="text" name="options"></td></tr>
	<tr><td>Comment:</td><td><input type="text" name="comment"></td></tr>
	<tr><td>Schedule</td><td>
					<select name="schedule">
						<option>daily</option>
						<option>weekly</option>
						<option>monthly</option>
					</select>
				</td></tr>
	<tr><td colspan="2"><input type="submit"></td></tr>
</table>
</form>
