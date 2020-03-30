/*
 Navicat Premium Data Transfer

 Source Server         : free_shark
 Source Server Type    : MySQL
 Source Server Version : 50645
 Source Host           : localhost:3306
 Source Schema         : free_shark

 Target Server Type    : MySQL
 Target Server Version : 50645
 File Encoding         : 65001

 Date: 01/12/2019 13:48:13
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `password` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `salt` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `email` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `activation` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '邮箱激活码',
  `type` int(255) NOT NULL COMMENT '0-表示用户，1-表示管理员',
  `status` int(255) NOT NULL COMMENT '0-表示未认证，1-表示认证',
  `create_time` datetime(0) NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

SET FOREIGN_KEY_CHECKS = 1;
-- ----------------------------
INSERT INTO `user` VALUES ('1', 'test1', 'pbkdf2:sha256:150000$MfyO9dm0$d7e23d2d8688bbec533de0ac24abcc41800c22e016a22409f6043ced5b55d3f5', 'salt', 'email', 'act', '1', '1', CURRENT_TIME());
INSERT INTO `user` VALUES ('2', 'test2', 'pbkdf2:sha256:150000$MfyO9dm0$d7e23d2d8688bbec533de0ac24abcc41800c22e016a22409f6043ced5b55d3f5', 'salt', 'xxx@xxx.com', 'act', '1', '1', CURRENT_TIME());
INSERT INTO `user` VALUES ('3', 'testAdmin', 'pbkdf2:sha256:150000$MfyO9dm0$d7e23d2d8688bbec533de0ac24abcc41800c22e016a22409f6043ced5b55d3f5', 'salt', 'yyy@yyy.com', 'act', '0', '1', CURRENT_TIME());