agents
- number - number, key
- name - string
- lastname - string
- phonenumber - string
- email - string
- business - string
- address_line1 - string
- address_line2 - string
- town - string
- county - string
- postcode - string
- siccode - string check



checksheet - not used
checksheet2 - not used

checksheet3
- number - number, key
- name - string
- location - string
- registration - string
- full_toilet_removed - number
- clean_toilet_cartridge_supplied - number
- new_soap_supplied_to_canteen_and_toilet - number
- new_hand_sanitiser_supplied_to_canteen_and_toilet - number
- toilet_flush_water_refilled - number
- hand_wash_water_refilled_and_dirty_water_emptied - number
- canteen_cleaned - number
- toilet_area_cleaned - number
- toilet_roll_supplied - number
- hand_towels_supplied - number

collection_point
- number - number, key
- name - string
- company - string
- address_line1 - string
- address_line2 - string
- town - string
- county - string
- postcode - string

customers - not used
locations - not used

login
- number - number, key
- username - string
- password - string
- pin - number

transferors
- number - number, key
- name - string
- lastname - string
- phonenumber - string 
- email - string
- business - string
- address_line1 - string
- address_line2 - string
- town - string
- county - string
- postcode - string
- siccode - string

users - used for /form-example
- name - string, key (probably)
- lastname - string
- email - string

waste_transfer
- number - number, key
- customer_name - string
- collection_point - string
- agent_name - string



CREATE TABLE `agents` (
	`number` INT NOT NULL AUTO_INCREMENT,
	`name` TEXT,
	`lastname` TEXT,
	`phonenumber` TEXT,
	`email` TEXT,
	`business` TEXT,
	`address_line1` TEXT,
	`address_line2` TEXT,
	`town` TEXT,
	`county` TEXT,
	`postcode` TEXT,
	`siccode` TEXT,
	PRIMARY KEY (`number`)
);

CREATE TABLE `transferors` (
	`number` INT NOT NULL AUTO_INCREMENT,
	`name` TEXT,
	`lastname` TEXT,
	`phonenumber` TEXT,
	`email` TEXT,
	`business` TEXT,
	`address_line1` TEXT,
	`address_line2` TEXT,
	`town` TEXT,
	`county` TEXT,
	`postcode` TEXT,
	`siccode` TEXT,
	PRIMARY KEY (`number`)
);

CREATE TABLE `collection_point` (
	`number` INT NOT NULL AUTO_INCREMENT,
	`name` TEXT,
	`company` TEXT,
	`address_line1` TEXT,
	`address_line2` TEXT,
	`town` TEXT,
	`county` TEXT,
	`postcode` TEXT,
	PRIMARY KEY (`number`)
);


CREATE TABLE `checksheet3` (
	`number` INT NOT NULL AUTO_INCREMENT,
	`name` TEXT,
	`location` TEXT,
	`registration` TEXT,
	`full_toilet_removed` INT,
	`clean_toilet_cartridge_supplied` INT,
	`new_soap_supplied_to_canteen_and_toilet` INT,
	`new_hand_sanitiser_supplied_to_canteen_and_toilet` INT,
	`toilet_flush_water_refilled` INT,
	`hand_wash_water_refilled_and_dirty_water_emptied` INT,
	`canteen_cleaned` INT,
	`toilet_area_cleaned` INT,
	`toilet_roll_supplied` INT,
	`hand_towels_supplied` INT,
	PRIMARY KEY (`number`)
);

CREATE TABLE `login` (
	`number` INT NOT NULL AUTO_INCREMENT,
	`username` TEXT,
	`password` TEXT,
	`pin` INT,
	PRIMARY KEY (`number`)
);

CREATE TABLE `login` (
	`number` INT NOT NULL AUTO_INCREMENT,
	`username` TEXT,
	`password` TEXT,
	`pin` INT,
	PRIMARY KEY (`number`)
);


INSERT INTO `login` (`username`,`password`,`pin`) VALUES ('admin','WIWAYBMFTMITCTSAMB','3264');  

CREATE TABLE `users` (
	`name` TEXT(60) NOT NULL,
	`lastname` TEXT,
	PRIMARY KEY (`name`)
);

CREATE TABLE `waste_transfer` (
	`number` INT NOT NULL AUTO_INCREMENT,
	`customer_name` TEXT,
	`collection_point` TEXT,
	`agent_name` TEXT,
	PRIMARY KEY (`number`)
);
