<?php

class datenfresser 
{

	function addContainer( $name, $comment, $path, $type, $options, $schedule, $group) 
	{
		$dbh = new PDO('sqlite:/var/datenfresser/datenfresser.db');
		$dbh->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_WARNING);
		
		try{
			$dbh->beginTransaction();
 			$dbh->query("INSERT INTO dataContainer(dataID,name,comment,localPath,remotePath,type,options,schedule,groupID) values ( NULL , '$name', '$comment', '$name' , '$path' , '$type', '$options', '$schedule' , '$group')");
			$dbh->commit();
			print "hallo";
  
		} catch (Exception $e) {
  			$dbh->rollBack();
  			echo "Failed: " . $e->getMessage();
		}
	}
}




?>
