CREATE DATABASE  IF NOT EXISTS `inventory`;
USE `inventory`;

CREATE TABLE IF NOT EXISTS `transactions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `amount` int NOT NULL,
  `type` varchar(45) NOT NULL,
  `description` varchar(100) DEFAULT NULL,
  `created_at` varchar(45) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `login` varchar(45) NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB;
