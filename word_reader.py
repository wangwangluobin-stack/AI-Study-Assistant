from docx import Document

def read_word(uploaded_file):

    doc = Document(uploaded_file)

    text = ""

    for para in doc.paragraphs:

        text += para.text + "\n"

    return text
