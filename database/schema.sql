#
# TABLE STRUCTURE FOR: quotes
#

CREATE TABLE `quotes` (
  `id` int(9) unsigned NOT NULL AUTO_INCREMENT,
  `author` varchar(255) NOT NULL,
  `text` text NOT NULL,
  KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;
