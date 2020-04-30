CREATE TABLE IF NOT EXISTS `ratings`(
   `userId` VARCHAR(4) NOT NULL,
   `movieId` VARCHAR(8) NOT NULL,
   `rating` FLOAT NOT NULL,
   `timestamp` VARCHAR(20),
   PRIMARY KEY ( `userId`, `movieId` )
);

CREATE TABLE IF NOT EXISTS `predictions`(
   `userId` VARCHAR(4) NOT NULL,
   `movieId` VARCHAR(8) NOT NULL,
   `rating` FLOAT NOT NULL,
   PRIMARY KEY ( `userId`, `movieId` )
);

CREATE TABLE IF NOT EXISTS `movies`(
   `movieId` VARCHAR(8) NOT NULL,
   `title` VARCHAR(256) NOT NULL,
   `genres` VARCHAR(256),
   `youtubeEmbedId` VARCHAR(128) DEFAULT 'bTqVqk7FSmY',
   PRIMARY KEY ( `movieId` )
);

ALTER TABLE `movies` ADD COLUMN `youtubeEmbedId` VARCHAR (128) DEFAULT 'bTqVqk7FSmY' COMMENT 'youtube embed Id'