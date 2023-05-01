/*
 Navicat Premium Data Transfer

 Source Server         : sz-aliyun
 Source Server Type    : MySQL
 Source Server Version : 50737
 Source Host           : 120.77.180.95:6306
 Source Schema         : air

 Target Server Type    : MySQL
 Target Server Version : 50737
 File Encoding         : 65001

 Date: 16/04/2023 15:58:52
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for sg_visibility
-- ----------------------------
DROP TABLE IF EXISTS `sg_visibility`;
CREATE TABLE `sg_visibility` (
  `station` char(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `visibility` float DEFAULT NULL,
  `pub_time` datetime NOT NULL,
  `CREATE_TIME` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `UPDATE_TIME` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE KEY `pub_station` (`pub_time`,`station`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Singapore weather observation data. temperature, relative humidity, wind.';

SET FOREIGN_KEY_CHECKS = 1;
