from langchain_community.document_loaders import (WebBaseLoader, YoutubeLoader, CSVLoader, PyPDFLoader, TextLoader)

def load_website(url):
    loader = WebBaseLoader(url, verify_ssl=False)
    documents = loader.load()
    return '\n\n'.join([doc.page_content for doc in documents])

def load_youtube(id_video):
    loader = YoutubeLoader(id_video, add_video_info=False, language=['pt'])
    documents = loader.load()
    return '\n\n'.join([doc.page_content for doc in documents])

def load_csv(file_path):
    loader = CSVLoader(file_path)
    documents = loader.load()
    return '\n\n'.join([doc.page_content for doc in documents])

def load_pdf(file_path):
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    return '\n\n'.join([doc.page_content for doc in documents])

def load_text(file_path):
    loader = TextLoader(file_path)
    documents = loader.load()
    return '\n\n'.join([doc.page_content for doc in documents])
