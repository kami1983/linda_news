CREATE TABLE `linda_news` (
  `id` int NOT NULL AUTO_INCREMENT,
  `item_id` int NOT NULL,
  `title` varchar(255) NOT NULL,
  `content` text NOT NULL,
  `author` varchar(255) NOT NULL,
  `publish_time` datetime NOT NULL,
  `uri` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `item_id` (`item_id`,`author`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `linda_news_category` (
  `id` int NOT NULL AUTO_INCREMENT,
  `news_id` int NOT NULL,
  `category` varchar(1000) DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `status` int DEFAULT '0',
  `csv_label` int DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `news_id` (`news_id`),
  KEY `status` (`status`)
) ENGINE=InnoDB AUTO_INCREMENT=411 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `linda_news_concepts` (
  `id` int NOT NULL AUTO_INCREMENT,
  `news_id` int NOT NULL,
  `concepts` varchar(1000) DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `status` int DEFAULT '0',
  `csv_label` int DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `news_id` (`news_id`),
  KEY `status` (`status`)
) ENGINE=InnoDB AUTO_INCREMENT=411 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



CREATE TABLE `linda_public_label` (
  `id` int NOT NULL AUTO_INCREMENT,
  `label` varchar(255) NOT NULL,
  `value` varchar(255) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `label` (`label`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- 记录CSV文件的更新日期，后面用于支持显示估值变化情况
CREATE TABLE `linda_csv_record` (
  `id` int NOT NULL AUTO_INCREMENT,
  `csv_label` int NOT NULL,
  `update_date` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `scv_label` (`csv_label`),
  KEY `update_date` (`update_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
