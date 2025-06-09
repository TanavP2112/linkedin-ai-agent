from PyPDF3 import PdfFileReader

def parse_resume(path):
    text = ""
    with open(path, "rb") as f:
        pdf_reader = PdfFileReader(f)
        for page in range(pdf_reader.getNumPages()):
            text += pdf_reader.getPage(page).extractText()
    return text