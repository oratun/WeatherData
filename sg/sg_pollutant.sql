/*
 Navicat Premium Data Transfer

 Source Server         : local
 Source Server Type    : MySQL
 Source Server Version : 80029
 Source Host           : localhost:3306
 Source Schema         : air

 Target Server Type    : MySQL
 Target Server Version : 80029
 File Encoding         : 65001

 Date: 06/06/2022 10:58:30
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for sg_pollutant
-- ----------------------------
DROP TABLE IF EXISTS `sg_pollutant`;
CREATE TABLE `sg_pollutant` (
  `STN` varchar(8) COLLATE utf8mb4_unicode_ci NOT NULL,
  `PUB_TIME` datetime NOT NULL,
  `PM25` float DEFAULT NULL,
  `PM10` float DEFAULT NULL,
  `SO2` float DEFAULT NULL,
  `O3` float DEFAULT NULL,
  `CO` float DEFAULT NULL,
  `NO2` float DEFAULT NULL,
  `CREATE_TIME` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `UPDATE_TIME` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE KEY `sg_pollutant_PUB_TIME_STN_uindex` (`PUB_TIME`,`STN`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

SET FOREIGN_KEY_CHECKS = 1;
