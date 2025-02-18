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
  PRIMARY KEY (`id`),
  UNIQUE KEY `news_id` (`news_id`),
  KEY `status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE `linda_news_concepts` (
  `id` int NOT NULL AUTO_INCREMENT,
  `news_id` int NOT NULL,
  `concepts` varchar(1000) DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `status` int DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `news_id` (`news_id`),
  KEY `status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
