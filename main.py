from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import JSONResponse
import os

from utils import loadPdf, loadVectorStore
from langchain_ollama import OllamaLLM
from langchain.chains import RetrievalQA

app = FastAPI()

vectorstore = None
qa_chain = None

@app.post("/upload/")
async def upload_pdf(file: UploadFile):
    global vectorstore, qa_chain

    file_path = f"data/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    chunks = loadPdf(file_path)
    vectorstore = loadVectorStore(chunks)

    llm = OllamaLLM(model="llama3.1:8b")
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        return_source_documents=False
    )
    print(qa_chain)
    return JSONResponse({"message": f"{file.filename} processed successfully!"})

@app.post("/ask/")
async def ask_question(question: str = Form(...)):
    global qa_chain
    if not qa_chain:
        return JSONResponse({"error": "No PDF uploaded yet!"}, status_code=400)

    response = qa_chain.invoke({"query": question})
    return JSONResponse({"answer": response["result"]})
