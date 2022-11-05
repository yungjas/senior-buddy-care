-- DB USES UTC TIME

CREATE TABLE `acceleration` (
    `acc_id` int NOT NULL AUTO_INCREMENT,
    `acc` float NOT NULL,
    `tilt` varchar(64) NOT NULL,
    `time_created` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(`acc_id`)
);

CREATE TABLE `weight` (
    `weight_id` int NOT NULL AUTO_INCREMENT,
    `weight_data` float NOT NULL,
    `time_created` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(`weight_id`)
);

CREATE TABLE `light` (
    `light_id` int NOT NULL AUTO_INCREMENT,
    `light_data` float NOT NULL,
    `time_created` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(`light_id`)
);