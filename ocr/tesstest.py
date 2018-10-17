from PIL import Image
import pytesseract

im = Image.open("ocrtestpic.PNG")

text = pytesseract.image_to_string(im, lang = 'eng')

print(text)
