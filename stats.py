from meneame.obtenerEstadisticas import obtenerEstadisticas
from meneame.utils import get_path
from meneame.properties import MENEAME_BASE_RSS
from meneame.properties import MENEAME_COMENTARIOS_RSS
from meneame.properties import MENEAME_PENDIENTES_RSS

path =  get_path()

stats_base 		  = obtenerEstadisticas(path, MENEAME_BASE_RSS)
stats_comentarios = obtenerEstadisticas(path, MENEAME_COMENTARIOS_RSS)
stats_pendientes  = obtenerEstadisticas(path, MENEAME_PENDIENTES_RSS)

stats_base.getStats()
stats_comentarios.getStats()
stats_pendientes.getStats()

