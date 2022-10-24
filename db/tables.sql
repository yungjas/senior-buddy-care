CREATE TABLE `acceleration` (
    `acc_id` int NOT NULL AUTO_INCREMENT,
    `acc_data` decimal(10, 9) NOT NULL,
    `time_created` DATETIME NULL,
    PRIMARY KEY(`acc_id`)
);

CREATE TABLE `weight` (
    `weight_id` int NOT NULL AUTO_INCREMENT,
    `weight_data` decimal(10, 9) NOT NULL,
    `time_created` DATETIME NULL,
    PRIMARY KEY(`weight_id`)
);

CREATE TABLE `light` (
    `light_id` int NOT NULL AUTO_INCREMENT,
    `light_data` decimal(10, 9) NOT NULL,
    `time_created` DATETIME NULL,
    PRIMARY KEY(`light_id`)
);