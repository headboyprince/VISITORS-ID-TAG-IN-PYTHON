# ALL THE MODULES NEEDED
import pandas as pd
import re  # import the regular expression python library
from PIL import Image, ImageDraw, ImageFont  # import the PIL library, from the PIL Library import the
# image draw, the image and the image font library
import textwrap

import time  # import the time library
from datetime import datetime  # import the datetime library

# %%
Name = input('\n what is your name: ')    # Name input box

def remove(Name):  #Ensure that the name inputted is in the correct format
    return "".join(Name.split())


no_space_name = remove(Name)
while not no_space_name.isalpha(): #no character, or numbers allowed, only alpahabets and space
    print('This isnt a real name, enter your real name please') #Print this if the incorrect name is entered
    Name = input('\n what is your name: ')
    no_space_name = remove(Name)

Name = Name.title() #make the name character inputted to be title case. so 'joe deo' will become 'John Deo'

Purpose = input("Enter your purpose [hint: "
                "i - interview,"
                "ii - meeting,"
                "iii - personal]: ")  # Purpose input box
Purpose = Purpose.capitalize() #capatilize the first letter of our input

def isValid(Phone):  # function to check if the phone number is a valid phone number
    # 1) Begins with 0, 1 or 91
    # 2) Then contains 7 or 8 or 9.
    # 3) Then contains 9 digits
    Pattern = re.compile("(0|1|91)?[7-9][0-9]{9}")
    return Pattern.match(Phone)
Phone = input("Enter your telephone digits: ")  # Phone number input box

while not (isValid(Phone)):
    # loop that will keep requesting for phone number until the correct phone number is entered.

    print("invalid phone number")
    # The message that will be printed out on the screen if an invalid number is entered.

    Phone = input("Enter your telephone digits: ")
    #the loop will ask for the phone number again if an invalid number is entered.

try:
    #ask the user to enter the name of the image that will be pasted on the template
    print('enter a valid image file, also make sure its stored in the photos folder')
    # enter the exact name of the image,

    photo = input("Enter image name: ")   # also make sure its stored in the photos folder.

except FileNotFoundError:
    #if the file wasnt found, catch the FileNotFoundError
    print('no file found')
    print('enter a valid image file, also make sure its stored in the photos folder')

    #also print this message informing the user that he should store the file in the photos folder
    while FileNotFoundError:    #loop to keep requesting for the input image file
        try:
            photo = input("Enter image name: ")

        except FileNotFoundError: #if the file wasnt found, catch the FileNotFoundError
            print('no file found')
            print('enter a valid image file, also make sure its stored in the photos folder')
        else:
            break #if the file is found break out from the while loop

else:
    pass # if the file is found, pass out from the first try, except loop

'''function for wrapping text that spans over one line into a box. 
we'll use it for the Purpose input to wrap it into the box provided for it.'''

ALLIGNMENT_LEFT = 0
ALLIGNMENT_CENTER = 1
ALLIGNMENT_RIGHT = 2
ALLIGNMENT_TOP = 3
ALLIGNMENT_BOTTOM = 4

def text_box(text, image_draw, font, box, horizontal_allignment, vertical_allignment,
             **kwargs):
    #function or wrapping the text into the box
    x = box[0]
    y = box[1]
    width = box[2]
    height = box[3]
    lines = text.split('\n')
    true_lines = []
    for line in lines:
        if font.getsize(line)[0] <= width:
            true_lines.append(line)
        else:
            current_line = ''
            for word in line.split(' '):
                if font.getsize(current_line + word)[0] <= width:
                    current_line += ' ' + word
                else:
                    true_lines.append(current_line)
                    current_line = word
            true_lines.append(current_line)
    true_lines[0]
    x_offset = y_offset = 0
    lineheight = font.getsize(true_lines[0])[1] * 1.2  # Give a margin of 0.2x the font height
    if vertical_allignment == ALLIGNMENT_CENTER:
        y = int(y + height / 2)
        y_offset = - (len(true_lines) * lineheight) / 2
    elif vertical_allignment == ALLIGNMENT_BOTTOM:
        y = int(y + height)
        y_offset = - (len(true_lines) * lineheight)

    for line in true_lines:
        linewidth = font.getsize(line)[0]
        if horizontal_allignment == ALLIGNMENT_CENTER:
            x_offset = (width - linewidth) / 2
        elif horizontal_allignment == ALLIGNMENT_RIGHT:
            x_offset = width - linewidth
        image_draw.text((int(x + x_offset), int(y + y_offset)), line, font=font, **kwargs)
        y_offset += lineheight

# %%
font = ImageFont.truetype("tempate-card-generator-master/OpenSans-Semibold.ttf",
                          size=25)  # the font used to layer the text on the card
# %%
template = Image.open("card visitors.JPG") # the template for the visitors card tag



# IMAGE BOX for the image to be posted on the template
pic = Image.open(f"tempate-card-generator-master/photos/{photo}.jpg").resize((175, 221), Image.ANTIALIAS)
#the photo to be pasted on each template

template.paste(pic, (534, 134, 709, 355)) #the image on each card
draw = ImageDraw.Draw(template)  # calling the draw function
draw.text((144, 98), Name, font=font, fill='black')  # Name box

draw.text((183, 380), Phone, font=font, fill='black')  # Phone box

text_box(Purpose, draw, font=font, box = (35, 218, 465, 312),
         horizontal_allignment = ALLIGNMENT_LEFT,
         vertical_allignment= ALLIGNMENT_LEFT, fill='black')  # Purpose box


current_time = time.strftime("%H:%M", time.localtime()) #function for the current time

current_date = datetime.now().date() #function for the exact date

draw.text((589, 379), str(current_time), font=font, fill='black')  # current time
draw.text((590, 81), str(current_date), font=font, fill='black')  # current date


template.save(f"tempate-card-generator-master/cards/{Name}.jpg")
# saving the template file with the name
