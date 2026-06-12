from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings

def get_embeddings():

    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

def create_chunks(pages):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )

    documents = []

    for page in pages:

        chunks = splitter.split_text(
            page["text"]
        )

        for chunk in chunks:

            documents.append(

                Document(
                    page_content=chunk,

                    metadata={
                        "page": page["page"]
                    }
                )

            )

    return documents