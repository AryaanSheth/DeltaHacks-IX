from PIL import Image, ImageFont, ImageDraw 
empty_img = Image.open("BlankCert.png")
# name = "Viransh Shah"
# courseName = "Java Basics"

def genCert(name, courseName):

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