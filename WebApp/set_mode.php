<?php


$url = "http://host:port/api/v1.0/system/automatic";
$data = array('type' => $_GET['mode']);


$options = array(
    'http' => array(
        'header'  => "Content-Type: application/json\r\n" .
                "Accept: application/json\r\n",
        'method'  => 'POST',
        'content' => json_encode($data)
    )
);
$context  = stream_context_create($options);
$result = file_get_contents($url, false, $context);


?>