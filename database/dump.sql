CREATE TABLE IF NOT EXISTS `students` (
  `id` int NOT NULL AUTO_INCREMENT,
  `roll_no` int NOT NULL,
  `name` varchar(100) NOT NULL,
  `father_name` varchar(100) NOT NULL,
  `mother_name` varchar(100) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `gender` enum('F','M') NOT NULL,
  `phone` varchar(100) DEFAULT NULL,
  `date_of_birth` DATE,
  `address` text,
  `class_id` int NOT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `teachers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `gender` enum('F','M') NOT NULL,
  `phone` varchar(100) DEFAULT NULL,
  `type` varchar(100) DEFAULT NULL,
  `date_of_birth` DATE,
  `address` text,
  PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `teacher_id` int DEFAULT NULL,
  `username` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `class` (
  `id` int NOT NULL AUTO_INCREMENT,
  `teacher_id` int NOT NULL,
  `name` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
);

ALTER TABLE `students` ADD CONSTRAINT FOREIGN KEY (`class_id`) REFERENCES `class`(`id`);
ALTER TABLE `users` ADD CONSTRAINT FOREIGN KEY (`teacher_id`) REFERENCES `teachers`(`id`);
ALTER TABLE `class` ADD CONSTRAINT FOREIGN KEY (`teacher_id`) REFERENCES `teachers`(`id`);