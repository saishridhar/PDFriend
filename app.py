import streamlit as st
from dotenv import load_dotenv
from pdfprocess import pdf2img, img2str


def main():
    load_dotenv()
    st.set_page_config(page_title='PDFriend', page_icon=':books:')

    st.header('Chat with PDFs')
    st.text_input('Query:')

    with st.sidebar:
      st.subheader('Your documents')
      docs = st.file_uploader('Upload PDF here and click Process', accept_multiple_files=True)
      if st.button('Process'):
         # get pdf text
         # get chunks
         # create vector store
         pass  

if __name__ == '__main__':
    main()