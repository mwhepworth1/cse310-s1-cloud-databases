-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema cse310-cloud-db
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `cse310-cloud-db` ;

-- -----------------------------------------------------
-- Schema cse310-cloud-db
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `cse310-cloud-db` DEFAULT CHARACTER SET utf8 ;
USE `cse310-cloud-db` ;

-- -----------------------------------------------------
-- Table `cse310-cloud-db`.`users`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `cse310-cloud-db`.`users` ;

CREATE TABLE IF NOT EXISTS `cse310-cloud-db`.`users` (
  `users_id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(45) NOT NULL,
  `pswd_hash` VARCHAR(255) NOT NULL,
  `picture_url` VARCHAR(45) NULL,
  PRIMARY KEY (`users_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `cse310-cloud-db`.`lists`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `cse310-cloud-db`.`lists` ;

CREATE TABLE IF NOT EXISTS `cse310-cloud-db`.`lists` (
  `lists_id` INT NOT NULL AUTO_INCREMENT,
  `list_name` VARCHAR(45) NOT NULL,
  `user_id` INT NULL,
  PRIMARY KEY (`lists_id`),
  UNIQUE INDEX `lists_id_UNIQUE` (`lists_id` ASC) VISIBLE,
  INDEX `lists_fk1_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `lists_fk1`
    FOREIGN KEY (`user_id`)
    REFERENCES `cse310-cloud-db`.`users` (`users_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `cse310-cloud-db`.`tasks`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `cse310-cloud-db`.`tasks` ;

CREATE TABLE IF NOT EXISTS `cse310-cloud-db`.`tasks` (
  `tasks_id` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(100) NOT NULL,
  `description` TEXT NOT NULL,
  `is_done` TINYINT NOT NULL,
  `list_id` INT NOT NULL,
  PRIMARY KEY (`tasks_id`),
  UNIQUE INDEX `tasks_id_UNIQUE` (`tasks_id` ASC) VISIBLE,
  UNIQUE INDEX `user_id_UNIQUE` (`list_id` ASC) VISIBLE,
  CONSTRAINT `tasks_fk1`
    FOREIGN KEY (`list_id`)
    REFERENCES `cse310-cloud-db`.`lists` (`lists_id`)
    ON DELETE NO ACTION 
    ON UPDATE NO ACTION) 
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `cse310-cloud-db`.`reminders`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `cse310-cloud-db`.`reminders` ;

CREATE TABLE IF NOT EXISTS `cse310-cloud-db`.`reminders` (
  `reminders_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  `task_id` INT NOT NULL,
  `due_date` DATETIME NOT NULL,
  PRIMARY KEY (`reminders_id`),
  UNIQUE INDEX `reminders_id_UNIQUE` (`reminders_id` ASC) VISIBLE,
  UNIQUE INDEX `user_id_UNIQUE` (`user_id` ASC) VISIBLE,
  UNIQUE INDEX `due_date_UNIQUE` (`due_date` ASC) VISIBLE,
  UNIQUE INDEX `task_id_UNIQUE` (`task_id` ASC) VISIBLE,
  CONSTRAINT `reminders_fk1`
    FOREIGN KEY (`task_id`)
    REFERENCES `cse310-cloud-db`.`tasks` (`tasks_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `reminders_fk2`
    FOREIGN KEY (`user_id`)
    REFERENCES `cse310-cloud-db`.`users` (`users_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
