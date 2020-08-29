
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for hko
-- ----------------------------
CREATE TABLE IF NOT EXISTS `hko` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `PUB_TIME` datetime DEFAULT NULL,
  `STN` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `WINDDIRECTION` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `WINDSPEED` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `GUST` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `TEMP` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `RH` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `MAXTEMP` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `MINTEMP` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `GRASSTEMP` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `GRASSMINTEMP` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `VISIBILITY` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `PRESSURE` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `TEMPDIFFERENCE` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  KEY `pub_time_name` (`PUB_TIME`,`STN`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

SET FOREIGN_KEY_CHECKS = 1;
