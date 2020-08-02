

from i2clibraries import i2c_lcd
from time import *
import urllib.request as ur
import json
import time

# Configuration parameters
# I2C Address, Port, Enable pin, RW pin, RS pin, Data 4 pin, Data 5 pin, Data 6 pin, Data 7 pin, Backlight pin (optional)
lcd = i2c_lcd.i2c_lcd(0x27,1, 2, 1, 0, 4, 5, 6, 7, 3)
url = "http://192.168.1.130:8080/dump1090-fa/data/aircraft.json"
now_old=0
messages_old=0

while True:
  try:
    no_of_aircrafts=0

    data = ur.urlopen(url)
    data_str=data.readall().decode('utf-8')
    data = json.loads(data_str)

    #count aircrafts which have a flight codes for aircraft in data'aircraft']:
    if "flight" in aircraft:
       no_of_aircrafts +=1

    #calculate messages/s      
    now=data'now']
    now_delta=now-now_old;
    messages=data'messages']
    messages_delta=messages-messages_old
    msps=round(messages_delta/now_delta,2)

    # If you want to disable the cursor, uncomment the following line
    lcd.command(lcd.CMD_Display_Control | lcd.OPT_Enable_Display)

    lcd.backLightOn()
    lcd.setPosition(1, 0)

    #format 1st line to 16 length
    string_line1="Aircrafts: "+str(no_of_aircrafts)
    string_line1='{0: <16}'.format(string_line1)   

    lcd.writeString(string_line1)
    lcd.setPosition(2, 0) 

    #format 2nd line to 16 length
    string_line2="Mess./s: " +str(msps)
    string_line2='{0: <16}'.format(string_line2)


    lcd.writeString(string_line2)
    now_old=now
    messages_old=messages
    time.sleep(10)

  #in case of network trouble continue
  except:  
    continue




