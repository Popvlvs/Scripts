<?php
$file = 'sess_klk75u2q4rpgfjs3785h6hpipp';
$contents = file_get_contents($file);
session_start();
session_decode($contents);
print_r($_SESSION);
?>
