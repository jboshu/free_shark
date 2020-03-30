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

 Date: 10/12/2019 17:23:12
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for commodity
-- ----------------------------
DROP TABLE IF EXISTS `commodity`;
CREATE TABLE `commodity`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `commodity_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '商品名称',
  `commodity_type` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '商品种类',
  `owner_student_id` varchar(15) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `price` float(10, 2) NOT NULL COMMENT '商品价格',
  `commodity_introduction` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '商品介绍',
  `commodity_photo_url1` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '商品实拍图1',
  `commodity_photo_url2` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '商品实拍图2',
  `commodity_photo_url3` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '商品实拍图3',
  `commodity_photo_url4` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '商品实拍图4',
  `commodity_photo_url5` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '商品实拍图5',
  `status` int(255) NULL DEFAULT 0 COMMENT '0-表示未售出，1-表示已经售出',
  `create_time` datetime(0) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `owner_student_id`(`owner_student_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 41 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of commodity
-- ----------------------------
INSERT INTO `commodity` VALUES (35, '小米手机', '手机', '2016141241188', 1599.00, '和我一起做米Boy', '/static/image/6d8f2a661b1b11ea98f0b0fc361748ec.jpg', '/static/image/6d8f78881b1b11ea9ea0b0fc361748ec.jpg', '/static/image/6d8fc6a61b1b11eabd95b0fc361748ec.jpg', '', '', 0, '2019-12-10 15:05:20');
INSERT INTO `commodity` VALUES (36, '牙刷', '生活必需品', '2016141241188', 10.00, '牙刷批发', '/static/image/61e52a521b1b11ea92e8b0fc361748ec.jpg', '/static/image/61e578741b1b11eaa3d2b0fc361748ec.jpg', '/static/image/61e5c6a61b1b11eabfd9b0fc361748ec.jpg', '', '', 0, '2019-12-10 15:05:00');
INSERT INTO `commodity` VALUES (37, '华为手机', '手机', '2016141225117', 3299.00, '爱我中华', '/static/image/52702d50174011eab11bb0fc361748ec.jpg', '/static/image/5270a274174011eab47cb0fc361748ec.jpg', '', '', '', 0, '2019-12-05 17:19:21');
INSERT INTO `commodity` VALUES (38, '脸盆', '生活必需品', '2016141225117', 15.00, '应有尽有，满足你洗脸洗脚的需求', '/static/image/6c0274a8174011eaae4bb0fc361748ec.jpg', '/static/image/6c02c2ca174011ea8939b0fc361748ec.jpg', '', '', '', 0, '2019-12-05 17:20:04');
INSERT INTO `commodity` VALUES (39, 'iphone', '手机', '2016141257442', 4288.00, '果粉看过来', '/static/image/b9e70d46174011ea813fb0fc361748ec.jpg', '/static/image/b9e75b5c174011eab6c2b0fc361748ec.jpg', '/static/image/b9e7d09e174011eaab98b0fc361748ec.jpg', '', '', 0, '2019-12-05 17:22:15');
INSERT INTO `commodity` VALUES (40, '机械键盘', '电子产品', '2016141225117', 429.00, '电竞键盘，打游戏，码代码，高效率', '/static/image/88ef31ae1b2e11ea9702b0fc361748ec.jpg', '/static/image/88efa7581b2e11ea9e40b0fc361748ec.jpg', '/static/image/88f01c661b2e11ea9e98b0fc361748ec.jpg', '', '', 0, '2019-12-10 17:22:06');

SET FOREIGN_KEY_CHECKS = 1;
