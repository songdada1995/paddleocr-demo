from paddleocr import PaddleOCR
import numpy as np
import cv2

# Initialize ocr_engine as None. It will be loaded on the first request.
ocr_engine = None

def get_ocr_engine():
    """
    Initializes and returns the PaddleOCR engine.
    This function ensures that the engine is a singleton.
    """
    global ocr_engine
    if ocr_engine is None:
        # The model will be downloaded automatically on the first run.
        ocr_engine = PaddleOCR(use_angle_cls=True, lang='ch')
    return ocr_engine

def run_ocr(image_bytes: bytes):
    """
    Performs OCR on the given image bytes.
    """
    engine = get_ocr_engine()
    # Convert image bytes to numpy array
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if img is None:
        return None

    result = engine.predict(img)
    return result