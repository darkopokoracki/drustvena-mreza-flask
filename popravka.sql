-- MySQL Script generated by MySQL Workbench
-- Fri 04 Feb 2022 09:54:35 AM CET
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema drustvena
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema drustvena
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `drustvena` DEFAULT CHARACTER SET utf8 ;
USE `drustvena` ;

-- -----------------------------------------------------
-- Table `drustvena`.`user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `drustvena`.`user` (
  `uderID` INT(11) NOT NULL,
  `firstName` VARCHAR(20) NOT NULL,
  `last_name` VARCHAR(30) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `username` VARCHAR(45) NOT NULL,
  `password` VARCHAR(200) NOT NULL,
  `profile_image` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`uderID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `drustvena`.`post`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `drustvena`.`post` (
  `postID` INT(11) NOT NULL,
  `title` VARCHAR(50) NOT NULL,
  `content` VARCHAR(200) NOT NULL,
  `image` VARCHAR(100) NOT NULL,
  `user_uderID` INT(11) NOT NULL,
  PRIMARY KEY (`postID`),
  INDEX `fk_post_user_idx` (`user_uderID` ASC) ,
  CONSTRAINT `fk_post_user`
    FOREIGN KEY (`user_uderID`)
    REFERENCES `drustvena`.`user` (`uderID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `drustvena`.`comment`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `drustvena`.`comment` (
  `commentID` INT(11) NOT NULL,
  `content` VARCHAR(150) NOT NULL,
  `post_postID` INT(11) NOT NULL,
  `user_uderID` INT(11) NOT NULL,
  PRIMARY KEY (`commentID`),
  INDEX `fk_comment_post1_idx` (`post_postID` ASC) ,
  INDEX `fk_comment_user1_idx` (`user_uderID` ASC) ,
  CONSTRAINT `fk_comment_post1`
    FOREIGN KEY (`post_postID`)
    REFERENCES `drustvena`.`post` (`postID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_comment_user1`
    FOREIGN KEY (`user_uderID`)
    REFERENCES `drustvena`.`user` (`uderID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `drustvena`.`likes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `drustvena`.`likes` (
  `likeID` INT(11) NOT NULL,
  `whom_liked` INT(11) NOT NULL,
  `post_postID` INT(11) NOT NULL,
  `who_liked` INT(11) NOT NULL,
  PRIMARY KEY (`likeID`),
  INDEX `post_postID` (`post_postID` ASC) ,
  INDEX `user_userID` USING BTREE (`whom_liked`) ,
  INDEX `fk_likes_user1_idx` (`who_liked` ASC) ,
  CONSTRAINT `fk_like_post1`
    FOREIGN KEY (`post_postID`)
    REFERENCES `drustvena`.`post` (`postID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `user_userID`
    FOREIGN KEY (`whom_liked`)
    REFERENCES `drustvena`.`user` (`uderID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_likes_user1`
    FOREIGN KEY (`who_liked`)
    REFERENCES `drustvena`.`user` (`uderID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
