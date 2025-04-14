import os
import fitz
from dataclasses import dataclass
from typing import List

@dataclass
class Document:
    """Data class for storing PDF document information."""
    id: int
    file_name: str
    content: str
    summary: str = None

def load_pdfs(folder_path: str) -> List[Document]:
    """
    Load all PDF files from MSS_AI_reports, extract text content from each, 
    and return a list of Document objects.
    """
    documents: List[Document] = []
    if not os.path.isdir(folder_path):
        return documents

    files = [f for f in os.listdir(folder_path) if f.lower().endswith(".pdf")]
    files.sort()
    for idx, file_name in enumerate(files):
        file_path = os.path.join(folder_path, file_name)
        try:
            doc = fitz.open(file_path)
            text = ""
            for page in doc:
                text += page.get_text()
                text += "\n"
            documents.append(Document(id=idx, file_name=file_name, content=text))
        except Exception as e:
            print(f"Warning: could not read file {file_name}: {e}")
        finally:
            try:
                doc.close()
            except:
                pass
    return documents