/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

-- Volcando estructura para tabla onv-server.eventos
CREATE TABLE IF NOT EXISTS `eventos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sucursal` int(11) NOT NULL,
  `timestamp` datetime NOT NULL DEFAULT current_timestamp() COMMENT 'timestamp (fecha y hora del evento)',
  `tipo` int(11) NOT NULL COMMENT '1: ingreso, 2: egreso',
  PRIMARY KEY (`id`),
  KEY `sucursal` (`sucursal`),
  CONSTRAINT `eventos_ibfk_1` FOREIGN KEY (`sucursal`) REFERENCES `sucursales` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=latin1;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla onv-server.sucursales
CREATE TABLE IF NOT EXISTS `sucursales` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) NOT NULL,
  `direccion` varchar(255) NOT NULL,
  `localidad` varchar(255) NOT NULL,
  `lat` varchar(60) NOT NULL,
  `lng` varchar(60) NOT NULL,
  `capacidad` int(11) NOT NULL,
  `encargado` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `encargado` (`encargado`),
  CONSTRAINT `sucursales_ibfk_1` FOREIGN KEY (`encargado`) REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=latin1;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para vista onv-server.sucursales_capacidad
-- Creando tabla temporal para superar errores de dependencia de VIEW
CREATE TABLE `sucursales_capacidad` (
	`sucursal` INT(11) NOT NULL,
	`capacidad` INT(11) NOT NULL,
	`ocupacion_actual` DECIMAL(23,0) NULL
) ENGINE=MyISAM;

-- Volcando estructura para tabla onv-server.usuarios
CREATE TABLE IF NOT EXISTS `usuarios` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(60) NOT NULL,
  `apellido` varchar(60) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `role` int(11) NOT NULL DEFAULT 0 COMMENT '0: sin permisos, 1: administrador, 2: encargado de sucursal',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para vista onv-server.sucursales_capacidad
-- Eliminando tabla temporal y crear estructura final de VIEW
DROP TABLE IF EXISTS `sucursales_capacidad`;
CREATE ALGORITHM=UNDEFINED SQL SECURITY DEFINER VIEW `sucursales_capacidad` AS select `eventos`.`sucursal` AS `sucursal`,`sucursales`.`capacidad` AS `capacidad`,sum(case when `eventos`.`tipo` = 1 then 1 else -1 end) AS `ocupacion_actual` from (`eventos` join `sucursales` on(`sucursales`.`id` = `eventos`.`sucursal`)) group by `eventos`.`sucursal`;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
