<?php

$url = "http://host:port/api/v1.0/change/device";
$uid = $_GET['uid'];
$mode = intval($_GET['mode']);
$data = array('devices' => array( array('uid' => $uid, 'motor' => $mode ) ));
$jdata = json_encode($data);

$options = array(
    'http' => array(
        'header'  => "Content-Type: application/json\r\n" .
                "Accept: application/json\r\n",
        'method'  => 'POST',
        'content' => $jdata
    )
);
$context  = stream_context_create($options);
$result = file_get_contents($url, false, $context);
echo($jdata);

?>