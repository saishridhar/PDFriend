import streamlit as st
from pdfprocess import multiprocessing,pdf2str
from langchain.text_splitter import CharacterTextSplitter
from encoder import store_in_vdb
from conversation import get_conversation_chain
from htmlTemplates import bot_template,user_template,css

def get_text_chunks(raw_text):
  text_splitter = CharacterTextSplitter(
     separator='\n',
     chunk_size=1000,
     chunk_overlap=200,
     length_function = len
  ) 
  chunks = text_splitter.split_text(raw_text)
  return chunks  

def handle_user_input(user_question):
   response = st.session_state.conversation({'question':user_question})
   st.write(user_template.replace('{{MSG}}',user_question),unsafe_allow_html=True)
   st.write(bot_template.replace('{{MSG}}',response['answer']),unsafe_allow_html=True)
   

def main():
    
    st.set_page_config(page_title='PDFriend', page_icon=':books:')
    
    st.write(css,unsafe_allow_html=True)


    if 'conversation' not in st.session_state:
       st.session_state.conversation = None
    st.header('Chat with PDFs')
    query = st.text_input('Query:')
    if query:
      handle_user_input(query)

    with st.sidebar:
      st.subheader('Your documents')
      docs = st.file_uploader('Upload PDF here and click Process', accept_multiple_files=True)
      if st.button('Process'):
         with st.spinner('Processing'):
         # get pdf text
          raw_text = pdf2str(docs) 
             
         # get chunks
          chunks = get_text_chunks(raw_text)
         # create vector store
         vdb = store_in_vdb(chunks)
         st.write('success!')
         st.session_state.conversation = get_conversation_chain(vdb)
         pass  

if __name__ == '__main__':
    multiprocessing.freeze_support()
    main()