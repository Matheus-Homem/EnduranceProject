CREATE TABLE `daily_control` (
  `entry_date` date NOT NULL,
  `user_id` varchar(36) NOT NULL,
  `element_category` varchar(255) NOT NULL,
  `element_name` varchar(255) NOT NULL,
  `has_data` tinyint(1) NOT NULL,
  PRIMARY KEY (`entry_date`,`user_id`,`element_category`,`element_name`),
  UNIQUE KEY `_control_uc` (`entry_date`,`user_id`,`element_category`,`element_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

CREATE TABLE `element_entries` (
  `id` int NOT NULL AUTO_INCREMENT,
  `entry_date` date NOT NULL,
  `user_id` varchar(36) NOT NULL,
  `element_category` varchar(255) NOT NULL,
  `element_name` varchar(255) NOT NULL,
  `element_string` text NOT NULL,
  `schema_encoded` text NOT NULL,
  `op` enum('c','u','d') NOT NULL DEFAULT 'c',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `_entry_uc` (`entry_date`,`user_id`,`element_category`,`element_name`)
) ENGINE=InnoDB AUTO_INCREMENT=57 DEFAULT CHARSET=utf8mb3;

CREATE TABLE `element_schemas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `element_category` varchar(255) NOT NULL,
  `element_name` varchar(255) NOT NULL,
  `schema_version` int NOT NULL,
  `schema_encoded` text NOT NULL,
  `schema_fields` text NOT NULL,
  `schema_dtypes` text NOT NULL,
  `op` enum('c','u','d') NOT NULL DEFAULT 'c',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `_schema_uc` (`element_category`,`element_name`,`schema_version`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb3;

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

