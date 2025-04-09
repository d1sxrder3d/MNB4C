import random
from captcha.image import ImageCaptcha



letters = ['А', 'Б', 'В','Ы','Ё','Е','К','Л','М',
           'Д','Н','Т','Ф','У','К',
           'Д','6','7','9','2','1','4']


def GenerateCaptchaPattern():
    sizeOfCaptcha = random.randint(4,5)

    pattern = [random.choice(letters) for _ in range(sizeOfCaptcha)]
    
    pattern = "".join(pattern)

    return pattern 


def GenerateCaptchaImage(pattern):

    image_captcha = ImageCaptcha(300, 200, font_sizes=[90])
    
    image_captcha.write(pattern, "captcha.png")
