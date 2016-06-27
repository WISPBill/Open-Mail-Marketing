<?php

$json = $_GET["geojson"];

$geo = json_decode($json);

$cords = $geo->geometry->coordinates;

$result = shell_exec('python getresult.py ' . escapeshellarg(json_encode($cords[0])));

$resultData = json_decode($result, true);

echo "$resultData";
?>