<?php

class datenfresser 
{

	var $db_string;
	var $db;

	function __construct( ) {
        	$this->db_string = 'sqlite:/var/datenfresser/datenfresser.db' ;
		$this->db = new PDO('sqlite:/var/datenfresser/datenfresser.db');
	}


	function get_running_jobs(){
		$dbh = $this->db;
		$dbh->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_WARNING);
		$data = $dbh->query("SELECT log.logID , log.start_timestamp , dataContainer.name FROM log,dataContainer WHERE log.status='running' AND log.dataID = dataContainer.dataID ");

		$log_id = $data->fetchAll(PDO::FETCH_ASSOC);

		return $log_id; 




	}

	function addContainer( $name, $comment, $path, $type, $options, $schedule, $group) 
	{
		$dbh = $this->db;
		$dbh->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_WARNING);
		
		try{
			$dbh->beginTransaction();
 			$dbh->query("INSERT INTO dataContainer(dataID,name,comment,localPath,remotePath,type,options,schedule,groupID) values ( NULL , '$name', '$comment', '$name' , '$path' , '$type', '$options', '$schedule' , '$group')");
			$dbh->commit();
  
		} catch (Exception $e) {
  			$dbh->rollBack();
  			echo "Failed: " . $e->getMessage();
		}
	}


	function deleteContainer( $id ){
		$dbh = $this->db;
		$dbh->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_WARNING);
		$data = $dbh->query("SELECT dataID FROM dataContainer WHERE dataID='".$id."'");
		if( sizeof($data->fetchAll(PDO::FETCH_ASSOC)) > 0){
				$dbh->query("DELETE FROM  dataContainer WHERE dataID='".$id."'");		
	
		}


	}


	function print_header()
	{
		print("<html>
			<head>
				<title>Datenfresser</title>
				<link rel='stylesheet' type='text/css' href='datenfresser.css'>
			</head>
			<body>");
		print(" <div id='banner'>
				<img src='images/small.png'>			
				<div id='banner_text'>
					<a href='datenfresser.php'>Show container</a>
					<a href='add_container.php'>Add container</a>
				</div>
			</div>
			<div height='300'>&nbsp;</div>
		
		");

	}
}




?>
