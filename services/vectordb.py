from langchain_community.vectorstores import Chroma

import shutil
import os

def create_vector_db(chunks, embeddings):

    return Chroma.from_documents(
        documents=chunks,
        embedding=embeddings
    )
