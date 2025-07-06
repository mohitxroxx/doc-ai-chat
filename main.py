from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import JSONResponse
import os

from utils import loadPdf, loadVectorStore
from langchain_ollama import OllamaLLM
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate


app = FastAPI()

vectorstore = None
qa_chain = None

custom_prompt = PromptTemplate(
    input_variables=["context", "question"],
    template = """
You are a helpful document assistant. Answer the question strictly based on the context provided below.

If the context does not contain relevant information to directly answer the question, and the question is general or opinion-based (not requiring concrete facts or claims), then you may generate an answer. In such cases, begin your answer with:

"Sorry, I'm unable to find any relevant response, but here's what I think:"

Do not invent facts from outside the context. If the question clearly requires factual information that is missing in the context, respond with:

"I'm sorry, I couldn't find relevant information in the document."

---

Context:
{context}

Question:
{question}

Answer:
"""
)


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
        return_source_documents=False,
        chain_type_kwargs={"prompt": custom_prompt}
    )
    print("qa_chain", qa_chain)
    return JSONResponse({"message": f"{file.filename} processed successfully!"})

@app.post("/ask/")
async def ask_question(question: str = Form(...)):
    global qa_chain
    if not qa_chain:
        return JSONResponse({"error": "No PDF uploaded yet!"}, status_code=400)

    response = qa_chain.invoke({"query": question})
    print("response", response)
    return JSONResponse({"answer": response["result"]})
