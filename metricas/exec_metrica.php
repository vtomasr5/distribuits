<?php
/**
*
*	Script PHP que ejecutara el script python con una llamada desde el navegador
*	exec_metrica.php?pw=CLAVE&nom=SUFIJO_METRICA
*	exec_metrica.php?pw=CLAVE&stop=1
*/
define("CLAVE" , "clave_ejecucion");
define("RUTA"  , "/home/meneame/distribuits/metricas/");
define("SCRIPT", "metricav2.py");

//Run linux command in background and return the PID created by the OS

if (isset($_GET['pw'])) {
	if ($_GET['pw'] == CLAVE) {
		$instruccion = "cd ".RUTA." && "; //Ejecutamos el comando desde el directorio
		if (!isset($_GET['stop'])) {
			if (isset($_GET['nom'])) {
				$instruccion .= "/usr/bin/python ".RUTA.SCRIPT." ".$_GET['nom'];
			} else {
				$instruccion .= "echo a";
			}
		} else { //Paramos la ejecución de los monitores
			$instruccion = "echo '' > ".RUTA.'exec.stop';			
		}

		$output = shell_exec($instruccion." > /dev/null 2>/dev/null &");
		print_r($output);
	}
}