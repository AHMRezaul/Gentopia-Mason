from gentopia.tools.basetool import BaseTool
from pydantic import BaseModel, Field
from typing import Optional, Type, AnyStr, Any
import PyPDF2
import requests

class PDFReaderArgs(BaseModel):
    file_path: str = Field(..., description="The path to the PDF file")

class PDFReader(BaseTool):
    """Tool to read PDF files and extract text content."""
    
    name = "pdf_reader"
    description = "Extracts text from a PDF file given a file path."

    args_schema: Optional[Type[BaseModel]] = PDFReaderArgs

    def _run(self, file_path: AnyStr) -> str:
        try:
            if file_path.startswith("http"):
                response = requests.get(file_path)
                if response.status_code == 200:
                    with open("downloaded.pdf", "wb") as pdf_file:
                        pdf_file.write(response.content)
                    file_path = "downloaded.pdf"
                else:
                    return f"Error downloading PDF: {response.status_code}"
            
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text()
            return text
        except Exception as e:
            return f"Error reading PDF: {e}"

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError


if __name__ == "__main__":
    pdf_reader = PDFReader()
    result = pdf_reader._run("https://arxiv.org/pdf/2407.02067")
    print(result)
