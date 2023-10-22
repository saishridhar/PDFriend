from langchain.embeddings import HuggingFaceBgeEmbeddings
import pinecone
from langchain.vectorstores import Pinecone
import os
from dotenv import load_dotenv


load_dotenv()

index_name = 'pdfstr'
model_name = 'BAAI/bge-small-en-v1.5'
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': True}


# initialize pinecone
pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"),  # find at app.pinecone.io
    environment=os.getenv("PINECONE_ENV"),  # next to api key in console
)

# First, check if our index already exists. If it doesn't, we create it
if index_name not in pinecone.list_indexes():
    # we create a new index
    pinecone.create_index(
      name=index_name,
      metric='cosine',
      dimension=384  
)
    
embeddings = HuggingFaceBgeEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)

def store_in_vdb(text):
    docsearch = Pinecone.from_texts(text, embeddings, index_name=index_name)
    return docsearch