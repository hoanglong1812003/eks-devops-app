from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    DirectoryLoader,
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from src.config import settings

def process_documents():
    # Load documents từ thư mục data
    loader = DirectoryLoader(f"{settings.DATA_PATH}/", glob="**/*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()

    # Thêm text files
    text_loader = DirectoryLoader(
        f"{settings.DATA_PATH}/",
        glob="**/*.txt",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
    )
    text_docs = text_loader.load()
    documents.extend(text_docs)

    # Chia nhỏ documents
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    texts = text_splitter.split_documents(documents)

    # Tạo embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name=settings.EMBEDDING_MODEL
    )

    # Tạo vector store
    vectorstore = FAISS.from_documents(texts, embeddings)
    vectorstore.save_local(settings.VECTORSTORE_PATH)

    print(f"Da xu ly {len(texts)} chunks tu {len(documents)} tai lieu")

if __name__ == "__main__":
    process_documents()
