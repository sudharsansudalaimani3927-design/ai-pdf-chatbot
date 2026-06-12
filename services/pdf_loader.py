from pypdf import PdfReader

def extract_pages(file_path):

    reader = PdfReader(file_path)

    pages = []

    for page_num, page in enumerate(reader.pages):

        page_text = page.extract_text()

        if page_text:

            pages.append(
                {
                    "page": page_num + 1,
                    "text": page_text
                }
            )

    return pages
