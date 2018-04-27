from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 

img = Image.open("images.jpg").convert("RGBA");
im = Image.open("logo.png").convert("RGBA");
im.thumbnail((100, 100), Image.ANTIALIAS);
im.save("temp.jpg",quality=100);
img.paste(im,(20,50),im)
draw = ImageDraw.Draw(img)
# font = ImageFont.truetype(<font-file>, <font-size>)
font = ImageFont.truetype("fonts/f1.ttf", 20)
	# draw.text((x, y),"Sample Text",(r,g,b))
i = input()
j = input()
k = input()
i = i + "\n"
j = j + "\n"
k = k + "\n"
draw.text((100,50),i,(0,0,0),font=font)
draw.text((100,80),j,(0,0,0),font=font)
draw.text((100, 110),k,(0,0,0),font=font)
img.save('power1.jpg')

