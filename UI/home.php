<!DOCTYPE html>
<html lang="en">

<head>
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/js/bootstrap.min.js"></script>
  <style>
  /* Style the input field */
  #myInput {
    padding: 20px;
    margin-top: -6px;
    border: 0;
    border-radius: 0;
    background: #f1f1f1;
  }
  #myBrandName {
    font-size: 30px;
	
  }
  </style>

  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <meta name="description" content="">
  <meta name="author" content="">

  <title></title>

  <!-- Bootstrap core CSS -->
  <link href="vendor/bootstrap/css/bootstrap.min.css" rel="stylesheet">

  <!-- Custom styles for this template -->
  <link href="css/business-frontpage.css" rel="stylesheet">

</head>

<body>

  <!-- Navigation -->
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top">
    <div class="container">
      <a id="myBrandName" class="navbar-brand" href="#">TravelGuide</a>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarResponsive" aria-controls="navbarResponsive" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarResponsive">
        <ul class="navbar-nav ml-auto">
          <li class="nav-item active">
            <a class="nav-link" href="#">Home
              <span class="sr-only">(current)</span>
            </a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#">About</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#">Services</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#">Contact</a>
          </li>
        </ul>
      </div>
    </div>
  </nav>

  <!-- Header -->
  <header class="bg-primary py-5 mb-5">
    <div class="container h-100">
      <div class="row h-100 align-items-center">
        <div class="col-lg-12">
          <h1 class="display-4 text-white mt-5 mb-2">Find all under one roof!!!</h1>
          <p class="lead mb-10 text-white" ><b>Having trouble deciding your next outing??? We help you choose the right place for right time!!!</b></p>
        </div>
      </div>
    </div>
  </header>

  <!-- Page Content -->
  <div class="container">

   
      <div class="col-md-11 mb-5">
         

     <div class="container">
  
	  <div class="dropdown">
		<button class="btn btn-primary dropdown-toggle" type="button" data-toggle="dropdown" id="stateSelector">Select State
		<span class="caret"></span></button>
		<ul class="dropdown-menu" id ="stateDrp">
		  <input class="form-control" id="myInput" type="text" placeholder="Search..">
		  <li><a href="#">COLORADO</a></li>
		</ul>
	  </div>
	</div>

<script>
$(function(){

    $("#stateDrp").on('click', 'li a', function(){
      $("#stateSelector:first-child").text($(this).text());
      $("#stateSelector:first-child").val($(this).text());
   });

});

$(document).ready(function(){
  $("#myInput").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $(".dropdown-menu li").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });
});
</script>
        <hr>
       
    <!-- /.row -->

    <div class="row">
      <?php
          error_reporting(E_ALL);
          ini_set('display_errors', true);
          ini_set('display_startup_errors', true);

          require 'vendor/autoload.php';
           
          $client = new MongoDB\Client("mongodb://localhost:27017");
          $collection = $client->DATASET->REVIEWS;
          $locations =  $collection->find(array(), array('projection' => array('NAME' => 1,"PROFILE_PIC_URL" => 1)));
          // $locNames = array();

          

          foreach($locations as $mongoid => $doc) {
              $tag = str_replace(' ' ,'',$doc["NAME"]);
              
             
              $image_data  = '<img class="card-img-top" src="'.$doc["PROFILE_PIC_URL"].'" alt="">';
              $data = "<div class='col-md-4 mb-5'>
                  <div class='card h-100'>".$image_data."
                  <div class='card-body'>
                      <h4 class='card-title'>";
                    // <img class='card-img-top' src='../dataset/testImage.jpeg' style='height:100%'' alt=''>
                    
              $data = $data.$doc["NAME"];
              $data = $data."</h4>
                      <p class='card-text'>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Sapiente esse necessitatibus neque sequi doloribus.</p>
                    </div>
                    <div class='card-footer'>
                      <a href='#'' class='btn btn-primary'>Find Out More!</a>
                    </div>
                  </div>
                </div>";
                echo $data;
          }


          ?>

    
    </div>
    <!-- /.row -->

  </div>
  <!-- /.container -->

  <!-- Footer -->
  

  <!-- Bootstrap core JavaScript -->
  <script src="vendor/jquery/jquery.min.js"></script>
  <script src="vendor/bootstrap/js/bootstrap.bundle.min.js"></script>

</body>

</html>

