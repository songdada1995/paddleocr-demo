from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from app.models.client import Client
from app.api import deps
from app.services import ocr_service

router = APIRouter()

@router.post("/recognize")
def recognize_text(
    *, 
    current_client: Client = Depends(deps.get_current_client),
    file: UploadFile = File(...)
):
    """
    Recognize text from an image.
    """
    contents = file.file.read()
    result = ocr_service.run_ocr(contents)
    
    if result is None or not result:
        raise HTTPException(status_code=400, detail="Invalid image file")

    # PaddleOCR 3.x predict 返回 list，每个元素是 dict，取第一个元素
    res = result[0]
    texts = res.get('rec_texts', [])
    scores = res.get('rec_scores', [])
    boxes = res.get('rec_polys', res.get('rec_boxes', []))

    processed_result = []
    for text, score, box in zip(texts, scores, boxes):
        processed_result.append({
            "box": box.tolist() if hasattr(box, 'tolist') else box,
            "text": text,
            "confidence": score
        })

    return {"result": processed_result}