# from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.ai.documentintelligence import DocumentIntelligenceClient

from azure.core.credentials import AzureKeyCredential
from dotenv import dotenv_values
from typing import List
from common import make_par


def adi_par_chunker(document_path:str, document_intelligence_client) -> List[dict]:
    
    with open(document_path, "rb") as f:
        poller = document_intelligence_client.begin_analyze_document("prebuilt-layout", analyze_request = f, output_content_format="text")
        

    result = poller.result()

    sub_documents = []
    content = None
    page = 0
    heading = ''
    headings = ['title', 'sectionHeading']

    for par in result.paragraphs:
        if par.role in headings:
            if content:
                paragraph = make_par(page, heading, content, document_path)
                sub_documents.append(paragraph)
            page = par.bounding_regions[0].page_number
            heading = par.content
            content = None
        
        if par.role is None:
            content = content + ' ' + par.content if content else par.content
    
    return sub_documents

def adi_md_chunker(document_path:str, document_intelligence_client) -> List[dict]:
    
    with open(document_path, "rb") as f:
        poller = document_intelligence_client.begin_analyze_document("prebuilt-layout", analyze_request = f, output_content_format="markdown")
        

    result = poller.result()

    # TBD from now on
    sub_documents = []
    content = None
    page = 0
    heading = ''
    headings = ['title', 'sectionHeading']

    for par in result.paragraphs:
        if par.role in headings:
            if content:
                paragraph = make_par(page, heading, content, document_path)
                sub_documents.append(paragraph)
            page = par.bounding_regions[0].page_number
            heading = par.content
            content = None
        
        if par.role is None:
            content = content + ' ' + par.content if content else par.content
    
    return sub_documents



def adi_chunker(document_path: str, method: str, dotenv_path='.env') -> List[dict]:

    config = dotenv_values(dotenv_path)
    credentials=AzureKeyCredential(config["adi_key"])
    document_intelligence_client = DocumentIntelligenceClient(endpoint=config["adi_endpoint"], credential=credentials)


    if method == 'adi_par':
        return adi_par_chunker(document_path, document_intelligence_client)
    
    elif method == 'adi_md':
        return [{}]
    
    else:
        raise ValueError(f"Unknown method {method}")
