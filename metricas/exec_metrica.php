<?php
/**
*
*	Script PHP que ejecutara el script python con una llamada desde el navegador
*	exec_metrica.php?pw=CLAVE
*	exec_metrica.php?pw=CLAVE&stop=1
*/
define("CLAVE", "clave_ejecucion");
$ruta	= '/home/meneame/distribuits/metricas/';
$script = 'metricav2.py';

//Run linux command in background and return the PID created by the OS

if (isset($_GET['pw'])) {
	if ($_GET['pw'] == CLAVE) {
		$instruccion = "cd ".$ruta." && ";
		if (!isset($_GET['stop'])) {
			$instruccion .= "/usr/bin/python ".$ruta.$script;
		} else {
			$instruccion = "echo '' > ".$ruta.'exec.stop';			
		}
		$output = shell_exec($instruccion." > /dev/null 2>/dev/null &");
		echo '<pre>';
		print_r($output);
		echo '</pre>';
	}
}