/*
 Navicat MySQL Data Transfer

 Source Server         : 115.28.18.59
 Source Server Type    : MySQL
 Source Server Version : 50547
 Source Host           : 115.28.18.59
 Source Database       : pdb

 Target Server Type    : MySQL
 Target Server Version : 50547
 File Encoding         : utf-8

 Date: 01/24/2017 16:37:31 PM
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
--  Table structure for `user`
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) DEFAULT NULL,
  `email` varchar(128) DEFAULT NULL,
  `password_hash` varchar(128) DEFAULT NULL,
  `school_id` int(11) DEFAULT NULL,
  `grade_id` int(11) DEFAULT NULL,
  `city_id` int(11) DEFAULT NULL,
  `province_id` int(11) DEFAULT NULL,
  `area_id` int(11) DEFAULT NULL,
  `user_type` int(11) DEFAULT NULL,
  `last_login_ip` varchar(64) DEFAULT NULL,
  `state` int(11) DEFAULT NULL,
  `phone` varchar(16) DEFAULT NULL,
  `code` varchar(12) DEFAULT NULL,
  `permissions` text,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `user`
-- ----------------------------
BEGIN;
INSERT INTO `user` VALUES ('1', 'test1', 'chenke91@qq.com', 'pbkdf2:sha1:1000$1NUPHryJ$a91577ec3c7c65be7d9e48b913d92ea69c916652', '1532', '10', '1258', '1257', '1266', null, null, '0', '18558707091', null, '[\"UPLOAD_PERMISSION\",\"CONFIRM_PERMISSION\", \"DEAL_PERMISSION\", \"INPUT_PERMISSION\", \"ANSWER_PERMISSION\", \"CHECK_PERMISSION\",\"JUDGE_PERMISSION\",\"VERIFY_PERMISSION\"]', '2016-12-26 21:29:19', '2016-12-26 21:29:19'), ('2', 'test2', 'chenke91@gmail.com', 'pbkdf2:sha1:1000$dnR27fq1$6fba30275ae5964367212ead1c0eddbb3e1b857e', '1532', '11', '1258', '1257', '1266', null, null, '0', '18559131924', null, '[\"UPLOAD_PERMISSION\"]', '2016-12-26 21:34:56', '2016-12-26 21:34:56');
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
