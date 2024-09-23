CREATE TABLE `element_entries` (
  `id` int NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `user_id` varchar(36) NOT NULL,
  `element_category` varchar(255) NOT NULL,
  `element_name` varchar(255) NOT NULL,
  `element_string` text NOT NULL,
  `schema_version` int NOT NULL,
  `op` enum('c','u','d') NOT NULL DEFAULT 'c',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `_entry_uc` (`date`,`user_id`,`element_category`,`element_name`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb3;

CREATE TABLE `element_schemas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `element_category` varchar(255) NOT NULL,
  `element_name` varchar(255) NOT NULL,
  `schema_version` varchar(64) NOT NULL,
  `schema_definition` text NOT NULL,
  `op` enum('c','u','d') NOT NULL DEFAULT 'c',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `_schema_uc` (`element_category`,`element_name`,`schema_version`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb3;

CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `user_id` varchar(36) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `user_id` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb3;

