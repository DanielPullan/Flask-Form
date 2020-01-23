Flask Form

This repo is half work, half reminder stuff for making CRUD applications in Python/Flask.

No fancy name or anything, just working code that will eventually be deployed to customers.

## Checksheet


```sql
CREATE TABLE `checksheet` (
`number` INT(4) NOT NULL AUTO_INCREMENT,
`name` VARCHAR(20),
`location` VARCHAR(20),
`registration` VARCHAR(20),
`full_toilet_removed` INT(1),
`clean_toilet_cartridge_supplied` INT(1),
`new_soap_supplied_to_canteen_and_toilet` INT(1),
`new_hand_sanitiser_supplied_to_canteen_and_toilet` INT(1),
`toilet_flush_water_refilled` INT(1),
`hand_wash_water_refilled_and_dirty_water_emptied` INT(1),
`canteen_cleaned` INT(1),
`toilet_area_cleaned` INT(1),
`toilet_roll_supplied` INT(1),
`hand_towels_supplied` INT(1),
PRIMARY KEY (`number`)
) ENGINE=InnoDB;
```