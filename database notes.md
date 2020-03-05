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
- siccode - string



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