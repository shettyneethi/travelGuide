<?php
error_reporting(E_ALL);
ini_set('display_errors', true);
ini_set('display_startup_errors', true);

 require 'vendor/autoload.php';
 // require 'simple_html_dom.php'
 
$client = new MongoDB\Client("mongodb://localhost:27017");
$collection = $client->DATASET->REVIEWS;
$locations =  $collection->find(array(), array('projection' => array('NAME' => 1)));
// $locNames = array();


function scrape_insta_hash($tag) {
	$dom = new DOMDocument();
	libxml_use_internal_errors(true);
	$dom->loadHTML('https://www.instagram.com/explore/tags/'.$tag.'/?_a=1');
	$data = $dom->getElementByTagName("pre");
	echo $data;
	// $insta_source = file_get_contents('https://www.instagram.com/explore/tags/'.$tag.'/?_a=1'); // instagram tag url
	// echo $insta_source;
}
$tag = str_replace(' ' ,'',"rockymountainnationalpark");
echo $tag;
scrape_insta_hash($tag);

	
// foreach($locations as $mongoid => $doc) {
// 	$tag = str_replace(' ' ,'',$doc["NAME"]);
// 	echo $tag;

// 	$results_array = scrape_insta_hash($tag);

	// $latest_array = $results_array['entry_data']['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_media']['edges'][0]['node'];
	// $image_data  = '<img class="card-img-top" src="'.$latest_array["thumbnail_src"].'" style="height:100%" alt="">';
	// echo $image_data;
	
// }







?>