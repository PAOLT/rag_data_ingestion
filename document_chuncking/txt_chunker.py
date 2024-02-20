from pypdf import PdfReader
from common import make_par

def format_text(text):
    text.replace("\n", " ")
    text.replace("\r", " ")
    text.replace("\t", " ")
    return text.split()

def txt_chunker(path, max_words: int = 1000, overlap: int = 200):
    sub_documents = []
    text = None
    n = 0
    reader = PdfReader(path)
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        page_text = page.extract_text()
        low = format_text(page_text)
        page_text = " ".join(low)
        text = text + ' ' + page_text if text else page_text
        n += len(low)
        if n>max_words:
            par = make_par(page=page_num, heading='na', content=text, file_name=path)
            sub_documents.append(par)
            text = " ".join(low[-overlap:])
            n = 200
    
    return sub_documents
        

# p = txt_chunker("document_chuncking/customer_docs/2PAA108438-600_A_en_System_800xA_Engineering_6.0_Application_Change_Management.pdf")
# print(len(p))