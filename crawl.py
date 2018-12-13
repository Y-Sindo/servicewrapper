from PIL import Image, ImageDraw, ImageFont

def get_image():
    pass
if __name__ == '__main__':
    im = Image.open("data/gaofen/screenshot.png")
    im2 =  Image.new("RGBA", (im.size[0], im.size[1]))
    draw = ImageDraw.Draw(im2)
    draw.rectangle((100, 100, 300, 600), fill=(0, 0, 255, 128))
    font = ImageFont.truetype("consola.ttf",size=40, encoding="unic")  # 设置字体
    draw.text((250,250),"1",font=font)
    blend = Image.alpha_composite(im, im2)
    blend.show()
    # c = draw.polygon([(0, 0), (0, 100), (100, 100), (200, 0)],fill=(255,0,0,1),outline=(255, 0, 0))

