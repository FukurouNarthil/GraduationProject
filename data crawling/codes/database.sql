create database IF NOT exists literature;
use literature;
DROP TABLE `regions`;
create table IF NOT EXISTS `regions` (  
	`region` VARCHAR(20) NOT NULL,     
    `period` VARCHAR(100),     
    `genre` VARCHAR(10),  
    `writer` VARCHAR(30),     
    `tags` VARCHAR(100),     
    `works` VARCHAR(100) 
);
select * from `regions`;
