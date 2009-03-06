<?php

class datenfresser 
{

	var $db_string;
	var $db;

	function __construct( ) {
        	$this->db_location = 'sqlite:/var/datenfresser/datenfresser.db' ;
		
		try{
		    $this->db = new PDO( $this->db_location );
		} catch (PDOException $e) {
		    $this->print_header();
		    $this->print_error_message( $e->getMessage() );
		    die();
		}
	}

	function print_error_message( $string ){
		print "<div id='error'>" . $string . "</div>";
	}


	function get_running_jobs(){
		$dbh = $this->db;
		$dbh->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_WARNING);
		$data = $dbh->query("SELECT log.logID , log.start_timestamp , dataContainer.name FROM log,dataContainer WHERE log.status='running' AND log.dataID = dataContainer.dataID ");

		$log_id = $data->fetchAll(PDO::FETCH_ASSOC);

		return $log_id; 
	}
	
	function get_volumes(){
		$dbh = $this->db;
		$dbh->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_WARNING);
		$data = $dbh->query("SELECT name FROM volumes");

		return $data->fetchAll( PDO::FETCH_COLUMN );
	}


	function addContainer( $name, $comment, $path, $type, $options, $volume, $schedule, $group,$archive,$compress,$archive_ttl) 
	{
		$dbh = $this->db;
		$dbh->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_WARNING);
		
		try{
			$dbh->beginTransaction();
 			$dbh->query("INSERT INTO dataContainer(dataID,name,comment,localPath,remotePath,type,options,schedule,groupID,archive,compress,archive_ttl,pre_command,post_command) values ( NULL , '$name', '$comment', '$name' , '$path' , '$type', '$options', '$schedule' , '$group','$archive','$compress','$archive_ttl','$pre_command','$post_command')");
			$dbh->commit();

			$dbh->beginTransaction();
			$data = $dbh->query("SELECT dataID FROM dataContainer WHERE name='". $name . "'");
			$container_id = $data->fetchAll(PDO::FETCH_COLUMN);
	
			$data = $dbh->query("SELECT volumeID FROM volumes WHERE name='". $volume . "'");
			$volume_id = $data->fetchAll(PDO::FETCH_COLUMN);

			print_r($volume_id);

			$dbh->query("INSERT INTO rel_volumes_container(volumeID,containerID) VALUES ('".$volume_id[0]."','".$container_id[0]. "')");
			
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
					<a href='index.php'>Show container</a>
					<a href='add_container.php'>Add container</a>
					<a href='show_volumes.php'>Volumes</a>
				</div>
			</div>
			<div height='300'>&nbsp;<br /><br /><br /><br /><br /></div>
		
		");

	}
}




?>
