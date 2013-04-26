<?php
/**
*
*	Script PHP que ejecutara el script python con una llamada desde el navegador
*	exec_metrica.php?pw=CLAVE
*/
define("CLAVE", "clave_ejecucion");
$ruta	= '/home/meneame/distribuits/metricas/'
$script = 'metrica.py'

if (isset($_GET['pw'])) {
	if ($_GET['pw'] == CLAVE) {
		exec("python ".$ruta.$script, $output);
		echo '<pre>';
		print_r($output);
		echo '</pre>';
	}
}