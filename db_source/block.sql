/*
Navicat MySQL Data Transfer

Source Server         : fs
Source Server Version : 80018
Source Host           : localhost:3306
Source Database       : free_shark

Target Server Type    : MYSQL
Target Server Version : 80018
File Encoding         : 65001

Date: 2019-12-12 16:30:43
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for block
-- ----------------------------
DROP TABLE IF EXISTS `block`;
CREATE TABLE `block` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `reason` varchar(255) DEFAULT NULL,
  `start_time` datetime NOT NULL,
  `end_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of block
-- ----------------------------
INSERT INTO `block` VALUES ('1', '5', '无可奉告！', '2019-12-12 15:24:38', '2019-12-12 15:24:38');
INSERT INTO `block` VALUES ('5', '6', '卖假货', '2019-12-10 15:43:18', '2019-12-11 15:43:21');
INSERT INTO `block` VALUES ('6', '2', '抹黑造谣', '2019-12-10 15:43:50', '2019-12-11 15:43:56');
INSERT INTO `block` VALUES ('7', '1', '敲诈勒索', '2019-12-06 15:44:10', '2019-12-08 15:44:14');
INSERT INTO `block` VALUES ('8', '7', '吃饭不付钱', '2019-12-12 15:46:49', '2019-12-14 15:46:49');
