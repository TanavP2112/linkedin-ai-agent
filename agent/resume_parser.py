import PyPDF3

def parse_resume(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        pdf_reader = PyPDF3.PdfReader(file)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text.strip()