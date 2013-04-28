<?php
/**
*
*	Script PHP que ejecutara el script python con una llamada desde el navegador
*	exec_metrica.php?pw=CLAVE
*	exec_metrica.php?pw=CLAVE&stop=1
*/
define("CLAVE", "clave_ejecucion");
$ruta	= '/home/meneame/distribuits/metricas/'
$script = 'metrica.py'

if (isset($_GET['pw'])) {
	if ($_GET['pw'] == CLAVE) {
		$instruccion = ''
		if (!isset($_GET['stop'])) {
			$instruccion = "python ".$ruta.$script;
		} else {
			$instruccion = "echo '' > ".$ruta.'exec.stop';			
		}
		exec($instruccion, $output);
		echo '<pre>';
		print_r($output);
		echo '</pre>';
	}
}