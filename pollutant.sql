SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for pollutant
-- ----------------------------
CREATE TABLE IF NOT EXISTS `pollutant` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `station_id` int(11) DEFAULT NULL,
  `station_name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `pub_time` datetime DEFAULT NULL COMMENT '数据发布时间',
  `NO2` float(8,2) DEFAULT NULL,
  `O3` float(8,2) DEFAULT NULL,
  `SO2` float(8,2) DEFAULT NULL,
  `CO` float(8,2) DEFAULT NULL,
  `PM10` float(8,2) DEFAULT NULL,
  `PM2.5` float(8,2) DEFAULT NULL,
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=34350849 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

SET FOREIGN_KEY_CHECKS = 1;
