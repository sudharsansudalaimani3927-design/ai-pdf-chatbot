from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

import shutil

from services.pdf_loader import extract_pages
from services.embeddings import (
    create_chunks,
    get_embeddings
)
from services.vectordb import create_vector_db
from services.rag import answer_question


app = FastAPI()

app.state.vector_db = None
app.state.status = "Idle"

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


@app.get("/", response_class=HTMLResponse)
def home():

    with open(
        "templates/index.html",
        "r",
        encoding="utf-8"
    ) as f:

        return f.read()


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    app.state.status = "📄 Uploading PDF"

    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    app.state.status += "<br>📖 Extracting Text"

    text = extract_pages(file_path)

    app.state.status += "<br>✂️ Creating Chunks"

    chunks = create_chunks(text)

    app.state.status += "<br>🧠 Generating Embeddings"

    embeddings = get_embeddings()

    app.state.status += "<br>🗄️ Creating Vector Database"

    app.state.vector_db = create_vector_db(
        chunks,
        embeddings
    )

    app.state.status += "<br>✅ Completed"

    return {
        "message": "PDF processed successfully",
        "chunks": len(chunks)
    }


@app.get("/status")
def get_status():

    return {
        "status": app.state.status
    }

@app.post("/ask")
async def ask_question(data: dict):

    if app.state.vector_db is None:

        return {
            "answer": "Please upload a PDF first.",
            "sources": []
        }

    result = answer_question(
        data["question"],
        app.state.vector_db
    )

    print("\nANSWER:")
    print(result["answer"])

    print("\nNUMBER OF SOURCES:")
    print(len(result["sources"]))

    return result

if __name__ == "__main__":
    import uvicorn
    import webbrowser

    webbrowser.open("http://localhost:8000")

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
    )
