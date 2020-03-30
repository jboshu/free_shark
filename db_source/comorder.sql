/*
 Navicat Premium Data Transfer

 Source Server         : free_shark
 Source Server Type    : MySQL
 Source Server Version : 80018
 Source Host           : localhost:3306
 Source Schema         : free_shark

 Target Server Type    : MySQL
 Target Server Version : 80018
 File Encoding         : 65001

 Date: 11/12/2019 16:42:37
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for comorder
-- ----------------------------
DROP TABLE IF EXISTS `comorder`;
CREATE TABLE `comorder`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `commodity_id` int(11) NOT NULL,
  `commodity_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `buyer_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `school_number` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `status` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '0-表示未处理，1-表示已同意，2-表示不同意',
  `create_time` datetime(0) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of comorder
-- ----------------------------
INSERT INTO `comorder` VALUES (1, 35, '小米手机', '2016141241188', '2016141225117', '0', '2019-12-04 13:15:16');
INSERT INTO `comorder` VALUES (2, 36, '牙刷', '2016141257442', '2016141241188', '0', '2019-12-03 13:15:33');
INSERT INTO `comorder` VALUES (3, 37, '华为手机', '2016141241188', '2016141257442', '1', '2019-12-08 15:30:41');
INSERT INTO `comorder` VALUES (4, 39, 'iphone', '2016141225117', '2016141241188', '1', '2019-12-08 15:31:03');
INSERT INTO `comorder` VALUES (5, 36, '牙刷', '2016141241188', '2016141225117', '2', '2019-12-04 16:31:51');
INSERT INTO `comorder` VALUES (6, 36, '牙刷', '2016141241188', '2016141257442', '0', '2019-12-27 16:35:32');

SET FOREIGN_KEY_CHECKS = 1;
