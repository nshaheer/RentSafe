from infrastructure.extractor import GVisionDocumentTextExtractor

def main():
   MyGV = GVisionDocumentTextExtractor()
   MyGV.extract_pdf_into_paragraphs(1, "/Users/SimarChawla/Downloads/333 Sample Lease.pdf")
   print("Hello")
   