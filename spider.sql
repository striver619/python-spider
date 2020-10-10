SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for house
-- ----------------------------
DROP TABLE IF EXISTS `house`;
CREATE TABLE `house` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL COMMENT '房屋名称',
  `price` decimal(10,2) DEFAULT NULL COMMENT '价格',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf16;

-- ----------------------------
-- Records of house
-- ----------------------------
BEGIN;
INSERT INTO `house` VALUES (1, 'demo', 12000.00);
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
