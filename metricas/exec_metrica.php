<?php
/**
*
*	Script PHP que ejecutara el script python con una llamada desde el navegador
*	exec_metrica.php?pw=CLAVE&nom=SUFIJO_METRICA
*	exec_metrica.php?pw=CLAVE
*	exec_metrica.php?pw=CLAVE&stop=1
*/
define("CLAVE" , "clave_ejecucion");
define("RUTA"  , "/home/meneame/distribuits/metricas/");
define("SCRIPT", "metricav2.py");

if (isset($_GET['pw'])) {
	if ($_GET['pw'] == CLAVE) {
		$instruccion = "cd ".RUTA." && "; //Ejecutamos el comando desde el directorio
		if (!isset($_GET['stop'])) {
			$nombre = '';
			if (isset($_GET['nom'])) {
				$nombre = $_GET['nom'];
			} else {
				$nombre = 'original';
			}
			$instruccion .= "/usr/bin/python ".RUTA.SCRIPT." ".$nombre;
		} else { //Paramos la ejecución de los monitores
			$instruccion = "echo '' > ".RUTA.'exec.stop';			
		}

		$output = shell_exec($instruccion." > /dev/null 2>/dev/null &");
		print_r($output);
	}
}