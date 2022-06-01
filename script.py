import pytesseract as tess
import cv2
import os

tess.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def ocr_core(src, language='rus+eng'):
    img = cv2.imread(os.path.abspath(os.path.dirname(__file__)) + src)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU |
                                 cv2.THRESH_BINARY_INV)
    cv2.fastNlMeansDenoising(thresh1, None, 50)
    cv2.imwrite('tmp/files/temps_files/threshold_image.jpg', thresh1)

    config = r'--oem 3 --psm 6'

    text = tess.image_to_string('tmp/files/temps_files/threshold_image.jpg', lang=language, config=config)

    if text:
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)) + "/tmp/files/temps_files/threshold_image.jpg")
        os.remove(path)

        path = os.path.join(os.path.abspath(os.path.dirname(__file__)) + src)
        os.remove(path)
        return text
    else:
        raise Exception('Can\'t find text on photo')
