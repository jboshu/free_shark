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

 Date: 10/12/2019 17:09:09
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for comment
-- ----------------------------
DROP TABLE IF EXISTS `comment`;
CREATE TABLE `comment`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `comment_content` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '评价内容',
  `commodity_id` int(11) NOT NULL COMMENT '商品id',
  `user_id` int(11) NOT NULL COMMENT '评论人的id',
  `username` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '评论人的用户名',
  `status` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '0' COMMENT '0-表示正常，1-表示被删除',
  `create_time` datetime(0) NOT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 13 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of comment
-- ----------------------------
INSERT INTO `comment` VALUES (2, '我觉得不行', 39, 1, 'test1', '0', '2019-12-09 15:56:04');
INSERT INTO `comment` VALUES (3, '我觉得OK啊', 39, 1, 'test1', '0', '2019-12-09 15:56:40');
INSERT INTO `comment` VALUES (4, '黑心商家实锤了', 39, 1, 'test1', '0', '2019-12-09 15:56:51');
INSERT INTO `comment` VALUES (5, '可以砍一刀吗', 39, 1, 'test1', '0', '2019-12-09 15:57:24');
INSERT INTO `comment` VALUES (6, '看着像用了很久了', 39, 1, 'test1', '0', '2019-12-09 15:59:55');
INSERT INTO `comment` VALUES (7, '不会是二手牙刷把', 36, 1, 'test1', '0', '2019-12-10 16:31:20');
INSERT INTO `comment` VALUES (8, '可以买多把吗', 36, 1, 'test1', '0', '2019-12-10 16:32:59');
INSERT INTO `comment` VALUES (9, '可以买多把吗', 36, 1, 'test1', '0', '2019-12-10 16:34:37');

SET FOREIGN_KEY_CHECKS = 1;
