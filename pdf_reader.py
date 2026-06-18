from pypdf import PdfReader


def read_pdf(uploaded_file):

    pdf = PdfReader(uploaded_file)

    text = ""

    for page in pdf.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text