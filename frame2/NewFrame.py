#!/usr/bin/env python
# coding: utf-8

import requests
import pandas as pd
from pandas import *
import os
import io
import csv
from PIL import Image, ImageFont, ImageDraw, ImageOps
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


# read CSV and select only name, id, photo
data = pd.read_csv("frameCSV.csv", usecols=["Name", "Student ID", "Upload Your decent Photo"])

# Create a client_secrets.json file with google OAuth 2.0
# auth using gmail
gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

for index, row in data.iterrows():
    # Save data from csv and download image
    student_name = str(row[0])
    student_id = str(row[1])
    student_image = str(row[2])
    file_id = student_image[33::]
    file_name = "{}-{}.png".format(student_name.split()[0], student_id)

    file2 = drive.CreateFile({'id': file_id})
    file2.GetContentFile(file_name)

    # Create mask for the picture
    im = Image.open(file_name)
    im = im.resize((500, 500))
    bigsize = (im.size[0] * 3, im.size[1] * 3)
    mask = Image.new('L', bigsize, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(im.size, Image.ANTIALIAS)
    im.putalpha(mask)

    # font selection
    title_font = ImageFont.truetype('font/font.ttf', 60)

    background = Image.open('template.png')
    image_editable = ImageDraw.Draw(background)
    image_editable.text((200, 800), student_name,
                        (252, 3, 40), font=title_font)
    image_editable.text((400, 900), student_id, (252, 3, 40), font=title_font)

    background.paste(im, (250, 200), im)
    # Save back with student name and id overwritting existing downloaded file
    background.save(file_name)
