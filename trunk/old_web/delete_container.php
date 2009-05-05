<?php

include("datenfresser_core.php");

$core = new datenfresser(); 
$core->print_header();

if( ! isset($_GET['id']) ) die("no id") ;

$core->deleteContainer( $_GET['id'] );


?>
