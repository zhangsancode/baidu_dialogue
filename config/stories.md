## happy path
* greet
  - utter_greet
* mood_great
  - utter_happy

## say goodbye
* goodbye
  - utter_goodbye

## ganen initiative
* begin_ganen
  - action_re_record
  
## ganen yes path
* yes
  - action_re_record
* record
  - action_re_record
* finish
  - utter_jili
  
## ganen no path 1
* no
  - utter_why_ganen
  - utter_tishi_ganen
* no
  - utter_quit_ganen
 
## ganen no path 2
* no
  - utter_why_ganen
  - utter_tishi_ganen
* yes
  - action_re_record
 
##
 
- utter_how_emotion