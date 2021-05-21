from PIL import Image, ImageDraw, ImageFont
from django.conf import settings
import os


def generate_certificate(nominal, number, user1, user2, user3):
    first_user = '1. {} {}'.format(user1.first_name, user1.last_name)
    second_user = '2. {} {}'.format(user2.first_name, user2.last_name)
    third_user = '3. {} {}'.format(user3.first_name, user3.last_name)
    number_text = '№' + str(number)
    init_image_name = 'cерт{}.webp'.format(nominal)
    if int(nominal) == 1:
        init_image_name = 'one.webp'
    image_path = os.path.join(settings.MEDIA_DIR, init_image_name)
    font_path = os.path.join(settings.MEDIA_DIR, 'font.ttf')
    img = Image.open(image_path)
    font = ImageFont.truetype(font_path, size=30)
    draw_text = ImageDraw.Draw(img)
    draw_text.text((17, 193), first_user, font=font)
    draw_text.text((57, 233), second_user, font=font)
    draw_text.text((112, 273), third_user, font=font)
    font_number = ImageFont.truetype("arial.ttf", 17)
    draw_text.text((272, 391), number_text, font=font_number, fill='black', stroke_width=1)
    file_name_result = '{}.webp'.format(number)
    file_name_result_path = os.path.join(settings.MEDIA_DIR, file_name_result)
    img.save(file_name_result_path)
    return file_name_result
