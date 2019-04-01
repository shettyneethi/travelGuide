<?php
error_reporting(E_ALL);
ini_set('display_errors', true);
ini_set('display_startup_errors', true);

 require 'vendor/autoload.php';
 
$client = new MongoDB\Client("mongodb://localhost:27017");
$collection = $client->DATASET->REVIEWS;
$locations =  $collection->find(array(), array('projection' => array('NAME' => 1)));
// $locNames = array();

foreach($locations as $mongoid => $doc) {
    
   $locNames[] = $doc["NAME"];
}
// foreach($locNames as $l) {
    
//   echo $l;
// }

?>