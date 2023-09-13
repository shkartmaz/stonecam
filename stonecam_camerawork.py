from PIL import Image, ImageOps, ImageEnhance
import os


stone = Image.open('pics/stone_1.JPG')
print(stone.size)
stone = ImageOps.grayscale(stone)
stoneEnhance = ImageEnhance.Contrast(stone)
stoneEnhance.enhance(10)
stone2 = Image.new(stoneEnhance, stone.size)

stone2.show()