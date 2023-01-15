from PIL import Image, ImageFont, ImageDraw 
import pandas as pd
import requests
import os

empty_img = os.path.join(os.path.dirname(__file__), "BlankCert.png")
# name = "Viransh Shah"
# courseName = "Java Basics"

def genCert(name : str,  courseName : str):

    font = ImageFont.truetype("DancingScript.ttf", 150)


    W,H = empty_img.size 
    w,h = font.getsize(name)
    w2,h2 = font.getsize(courseName)

    if W%w < 2: 
        font_size = 150 
        width = ((W-w)/2)
        height = ((H-h)/2)-50
    else: 
        font_size = 130
        width = ((W-w)/2) +75
        height = ((H-h)/2)-10

    print(W%w2)
    if W%w2 < 2: 
        font_size2 = 70 
        width2 = ((W-w2)/2) 
        height2 = ((H-h2)/2)+80
    else:
        font_size2 = 50
        width2 = ((W-w2)/2) +75
        height2 = ((H-h2)/2)+100

    font = ImageFont.truetype("DancingScript.ttf", font_size)
    font2 = ImageFont.truetype("Arial Unicode.ttf", font_size2)
    image_editable = ImageDraw.Draw(empty_img)
    image_editable.multiline_text((width,height+60), name, (35, 57, 75), font=font)
    image_editable.multiline_text((width2 + (w2//3) - 70,height2+260), courseName, (35, 57, 75), font=font2)
    empty_img.save("result.png")

    url = "https://api.verbwire.com/v1/nft/mint/mintFromFile"

    files = {"filePath": ("result.png", open("result.png", "rb"), "image/png")}
    payload = {
        "allowPlatformToOperateToken": "true",
        "chain": "goerli",
        "contractAddress": "0x002511aD5e6A8E24aCa9872579Ef8C46944ab4CD",
        "name": f"{name}'s Certificate",
        "description": f"Certificate of completion for {courseName}",
        "recipientAddress": "0x466228a573ea23f97476cae9b7e54e4b1f7114b7"
    }
    headers = {
        "accept": "application/json",
        "X-API-Key": "sk_live_d81b68aa-cf30-4ae9-a022-7de89eaf81bf"
    }

    response = requests.post(url, data=payload, files=files, headers=headers)

    return 'https://testnets.opensea.io/collection/asad-lj3lkc9wpf'
