# Updated ocrServices.py
import easyocr
import numpy as np
import cv2
from paddleocr import PaddleOCR
import pytesseract
from pyocr import pyocr
from pyocr.builders import TextBuilder
from PIL import Image

class ImageTextExtractor:
    def __init__(self, languages=['en']):
        self.easyocr_reader = easyocr.Reader(languages)
        self.paddleocr_reader = PaddleOCR(use_angle_cls=True, lang='en')
        self.pyocr_tool = pyocr.get_available_tools()[0] if pyocr.get_available_tools() else None

    def extract_text_easyocr(self, image_bytes):
        np_arr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        results = self.easyocr_reader.readtext(image)
        return [text for (_, text, _) in results]

    def extract_text_paddleocr(self, image_bytes):
        np_arr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        results = self.paddleocr_reader.ocr(image, cls=True)
        return [line[1][0] for line in results[0]]

    def extract_text_tesseract(self, image_bytes):
        np_arr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        return pytesseract.image_to_string(image)

    def extract_text_pyocr(self, image_bytes):
        if not self.pyocr_tool:
            return "PyOCR tool not available."

        np_arr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        return self.pyocr_tool.image_to_string(pil_image, builder=TextBuilder())

    def extract_text_all(self, image_bytes):
        return {
            "easyocr": self.extract_text_easyocr(image_bytes),
            "paddleocr": self.extract_text_paddleocr(image_bytes),
            "tesseract": self.extract_text_tesseract(image_bytes),
            "pyocr": self.extract_text_pyocr(image_bytes)
        }
