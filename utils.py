import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

def loadPdf(path: str):
    loader = PyPDFLoader(path)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = splitter.split_documents(documents)
    return chunks

def get_embeddings_model():
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def loadVectorStore(chunks, path="vectorstore/"):
    os.makedirs(path, exist_ok=True)
    embeddings = get_embeddings_model()

    if os.path.exists(os.path.join(path, "index.faiss")):
        return FAISS.load_local(path, embeddings, allow_dangerous_deserialization=True)
    
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(path)
    return vectorstore
