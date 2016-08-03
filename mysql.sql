CREATE TABLE `otstatis_noveseek` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `name` varchar(500) NOT NULL COMMENT '小说名字',
  `chapter` varchar(500) NOT NULL COMMENT '章节',
  `updatetime` datetime NOT NULL COMMENT '更新时间',
  `create_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `modify_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '修改时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8 COMMENT='小说抓取';
