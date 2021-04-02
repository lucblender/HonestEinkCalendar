#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd5in83b_V2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

import GCalendarEvents

from datetime import datetime
import calendar

DEBUG_PICTURE = False
HIGHLIGHT_SEQU = "!h"

logging.basicConfig(level=logging.DEBUG)

def crop_text(text, font_local, size):
    w, h = drawblack.textsize(text, font = font_local) 
    if w > size:
        remove_char = 3
        while drawblack.textsize(text[:-remove_char]+"...", font = font_local)[0] > size:
            remove_char+=1
        return text[:-remove_char]+"..."
    else:
        return text    

try:
    logging.info("epd5in83b_V2 Demo")
    
    epd = epd5in83b_V2.EPD()
    logging.info("init and Clear")
    if DEBUG_PICTURE == False:
        epd.init()
        epd.Clear()
    
    # Drawing on the image
    logging.info("Drawing")    
    font24 = ImageFont.truetype(os.path.join(picdir, '/home/pi/FONT/Noir/NoirStd-Regular.ttf'), 24)
    font18 = ImageFont.truetype(os.path.join(picdir, '/home/pi/FONT/Noir/NoirStd-Regular.ttf'), 18)
    fontNoir24 = ImageFont.truetype(os.path.join(picdir, '/home/pi/FONT/Noir/NoirStd-Regular.ttf'), 24)
    fontNoir50 = ImageFont.truetype(os.path.join(picdir, '/home/pi/FONT/Noir/NoirStd-Regular.ttf'), 50)
    fontNoir65 = ImageFont.truetype(os.path.join(picdir, '/home/pi/FONT/Noir/NoirStd-Regular.ttf'), 65)
    fontNoir45 = ImageFont.truetype(os.path.join(picdir, '/home/pi/FONT/Noir/NoirStd-Regular.ttf'), 45)
    fontNoir18 = ImageFont.truetype(os.path.join(picdir, '/home/pi/FONT/Noir/NoirStd-Regular.ttf'), 18)
    fontNoir30 = ImageFont.truetype(os.path.join(picdir, '/home/pi/FONT/Noir/NoirStd-Regular.ttf'), 30)
    
    # Drawing on the Horizontal image
    logging.info("1.Drawing on the Horizontal image...") 
    HBlackimage = Image.open('/home/pi/e-ink-calendar-b.bmp')
    HRYimage = Image.open('/home/pi/e-ink-calendar-r.bmp')
    drawblack = ImageDraw.Draw(HBlackimage)
    drawry = ImageDraw.Draw(HRYimage)
    
    today  =datetime.today()
    now = datetime.now()
    first_day = datetime(today.year, today.month, 1)

    day_in_month = calendar.monthrange(now.year, now.month)[1]
    week_number = today.isocalendar()[1]
    
    offset_calendar_nb_x = 335
    offset_calendar_nb_y = 175
    calendar_offset_y = 40
    
    events = GCalendarEvents.getEvents()
    index = 0
    
    
    if len(events) == 0:
        drawblack.text((offset_calendar_nb_x, offset_calendar_nb_y+20),  "Your calendar is", font = fontNoir30, fill = 0)  
        drawry.text((offset_calendar_nb_x, offset_calendar_nb_y+65),  "FUCKING", font = fontNoir50, fill = 1)   #REED
        drawblack.text((offset_calendar_nb_x+206, offset_calendar_nb_y+85),  "empty.", font = fontNoir24, fill = 0)  
        
        drawblack.text((offset_calendar_nb_x, offset_calendar_nb_y+160),  "You can stay in", font = fontNoir24, fill = 0)  
        drawry.text((offset_calendar_nb_x+186, offset_calendar_nb_y+160),  "bed!", font = fontNoir24, fill = 1)   #REED   
    else:    
        for event in events:
            if index == 5:
                msg_time = "..."
                drawry.text((offset_calendar_nb_x, offset_calendar_nb_y+index*calendar_offset_y),  msg_time, font = fontNoir24, fill = 1)            
            else:
                start = event['start'].get('dateTime', event['start'].get('date'))
                start_datetime = datetime.fromisoformat(start)
                msg_time = start_datetime.strftime("%H:%M")
                
                drawry.text((offset_calendar_nb_x, offset_calendar_nb_y+index*calendar_offset_y),  msg_time, font = fontNoir24, fill = 1)
                if HIGHLIGHT_SEQU in event['summary']:
                    highlight_event = event['summary'].replace(HIGHLIGHT_SEQU, "")                
                    summary_cropped = crop_text(highlight_event, fontNoir24, 220)
                    drawry.text((offset_calendar_nb_x + 70, offset_calendar_nb_y+index*calendar_offset_y),  summary_cropped, font = fontNoir24, fill = 1)
                else:
                    summary_cropped = crop_text(event['summary'], fontNoir24, 220)
                    
                    drawblack.text((offset_calendar_nb_x + 70, offset_calendar_nb_y+index*calendar_offset_y),  summary_cropped, font = fontNoir24, fill = 0)
            index+=1

    offset_calendar_nb_x = 35
    offset_calendar_nb_y = 250
    number_offset_x = 40
    number_offset_y = 40
    day_of_week = first_day.weekday()
    
    days_short = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
    days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    
    
    for x in range(0,7):
        msg = days_short[x]
        w, h = drawblack.textsize(msg, font = fontNoir18,)
        drawblack.text((offset_calendar_nb_x+number_offset_x*x-(w/2), offset_calendar_nb_y-number_offset_y-(h/2)), msg, font = fontNoir18, fill = 0)
    
    
    for y in range(0,6):
        for x in range(0,7):
            day_number = 7*y+(x+1)-day_of_week
            if(day_number<1):
                day_number = ""
            elif(day_number>day_in_month):
                day_number = ""
                
            
            msg = str(day_number)
            
            if day_number == today.day:
                w, h = drawblack.textsize(msg, font = fontNoir18)
                radius = 10
                x_start = offset_calendar_nb_x+number_offset_x*x
                y_start = offset_calendar_nb_y+number_offset_y*y
                drawry.chord((x_start-radius, y_start-radius, x_start+radius, y_start+radius), 0, 360, fill = 1)
                w, h = drawblack.textsize(msg, font = fontNoir18,)
                drawry.text((x_start-(w/2), y_start-(h/2)), msg, font = fontNoir18, fill = 0)
                
            else:
                w, h = drawblack.textsize(msg, font = fontNoir18,)
                drawblack.text((offset_calendar_nb_x+number_offset_x*x-(w/2), offset_calendar_nb_y+number_offset_y*y-(h/2)), msg, font = fontNoir18, fill = 0)
            
    offset_x = 20
    offset_y = 20
    
    highlight_event = None
    
    for event in events:
        if HIGHLIGHT_SEQU in event['summary']:
            highlight_event = event['summary'].replace(HIGHLIGHT_SEQU, "")
            break
                
    if highlight_event!= None:
        drawblack.text((offset_x, offset_y),  "Hey, you have an", font = fontNoir24, fill = 0)
        drawry.text((offset_x, 48+offset_y), "IMPORTANT", font = fontNoir30, fill = 1)       #todo_red     
        drawblack.text((170+offset_x, 55+offset_y), "event:", font = fontNoir18, fill = 0)  
        cropped_highlight_event = crop_text(highlight_event, fontNoir45, 300)        
        drawblack.text((offset_x, 80+offset_y), cropped_highlight_event, font = fontNoir45, fill = 0)     
    else:
        if day_of_week<5: #weekend message
            drawblack.text((offset_x, offset_y),  "Happy fucking week", font = fontNoir24, fill = 0)
            drawblack.text((offset_x, 55+offset_y), "Go to", font = fontNoir18, fill = 0)      
            drawry.text((50+offset_x, 20+offset_y), "work", font = fontNoir65, fill = 1)        
            drawblack.text((offset_x, 80+offset_y), "goddamn!", font = fontNoir50, fill = 0)        
        else:   # week message
            if week_number%2 == 0:
                drawblack.text((offset_x, offset_y),  "Weekend!", font = fontNoir24, fill = 0)
                
                drawblack.text((offset_x, 55+offset_y), "Put the", font = fontNoir18, fill = 0)      
                drawry.text((60+offset_x, 20+offset_y), "GLASS", font = fontNoir65, fill = 1)        
                drawblack.text((offset_x, 80+offset_y), "to the trash!", font = fontNoir45, fill = 0)     
            else:            
                drawblack.text((offset_x, offset_y),  "Weekend!", font = fontNoir24, fill = 0)
                
                drawblack.text((offset_x, 55+offset_y), "Put the", font = fontNoir18, fill = 0)      
                drawry.text((60+offset_x, 20+offset_y), "PAPER", font = fontNoir65, fill = 1)        
                drawblack.text((offset_x, 80+offset_y), "to the trash!", font = fontNoir45, fill = 0)    
        
    
    w, h = drawblack.textsize(today.strftime("%A"), font = fontNoir50)    
    drawblack.text((epd.width-10-w, 10),  today.strftime("%A"), font = fontNoir50, fill = 1)
    w_m, h_m = drawry.textsize(today.strftime(" %B"), font = fontNoir45)    
    w_d, h_d = drawry.textsize(today.strftime("%d"), font = fontNoir45)    
    
    drawblack.text((epd.width-10-w_m, 60), today.strftime(" %B"), font = fontNoir45, fill = 1)
    drawry.text((epd.width-10-w_m, 60), today.strftime(" %B"), font = fontNoir45, fill = 1)
    
    drawblack.text((epd.width-10-w_m-w_d, 60), today.strftime("%d"), font = fontNoir45, fill = 1)
    
    
    if DEBUG_PICTURE == False:
        epd.display(epd.getbuffer(HBlackimage), epd.getbuffer(HRYimage))
        logging.info("Goto Sleep...")
        epd.sleep()
    else:
        HBlackimage.save("HBlackimage.png")
        HRYimage.save("HRYimage.png")

        
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd5in83b_V2.epdconfig.module_exit()
    exit()
