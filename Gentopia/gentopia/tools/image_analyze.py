from gentopia.tools.basetool import *
from pydantic import BaseModel, Field
from typing import Optional, Type, AnyStr, Any
import pytesseract
from PIL import Image
import requests
from io import BytesIO

class ImageAnalysisArgs(BaseModel):
    image_url: str = Field(..., description="The URL of the image to analyze")

class ImageAnalysisTool(BaseTool):
    """Tool to download and analyze images for extracting text."""

    name = "image_analysis"
    description = "Downloads an image from a URL and performs analysis (OCR) to extract text."

    args_schema: Optional[Type[BaseModel]] = ImageAnalysisArgs

    def _run(self, image_url: AnyStr) -> str:
        try:
            response = requests.get(image_url)
            if response.status_code == 200:
                img = Image.open(BytesIO(response.content))
                
                extracted_text = pytesseract.image_to_string(img)

                return f"Extracted Text from Image:\n{extracted_text}"
            else:
                return f"Failed to download image, HTTP status code: {response.status_code}"
        except Exception as e:
            return f"Error analyzing image: {e}"

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError


if __name__ == "__main__":
    image_analyzer = ImageAnalysisTool()
    image_url = "https://i.sstatic.net/IvV2y.png"
    result = image_analyzer._run(image_url)
    print(result)
