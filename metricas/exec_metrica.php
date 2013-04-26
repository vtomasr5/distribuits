<?php

$ruta	= '/home/meneame/distribuits/metricas/'
$script = 'metrica.py'

exec("python ".$ruta.$script, $output);
echo '<pre>';
print_r($output);
echo '</pre>';