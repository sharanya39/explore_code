import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
#from langchain.vectorstores import FAISS
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain_openai import OpenAI
from langchain_community.chat_models import ChatOpenAI
#from langchain.callbacks import get_openai_callback
from langchain_community.callbacks.manager import get_openai_callback
import docx2txt
import os
import warnings
import pandas as pd

# Suppress warnings
warnings.filterwarnings('ignore')

def app():
    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    st.header("Ask your Documents 💬")

    # Upload files
    uploaded_files = st.file_uploader("Upload your files", type=["pdf", "txt", "docx"], accept_multiple_files=True)
    
    # Extract text from uploaded files
    all_text = ""
    for uploaded_file in uploaded_files:
        if uploaded_file.type == "application/pdf":
            pdf_reader = PdfReader(uploaded_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
        elif uploaded_file.type == "text/plain":
            text = uploaded_file.read().decode("utf-8")
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            text = docx2txt.process(uploaded_file)
        else:
            st.write(f"Unsupported file type: {uploaded_file.name}")
            continue
        all_text += text

    # Split text into chunks
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=3000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(all_text)

    # Check if chunks are created correctly
    if not chunks:
        #st.write("No text chunks created. Please check the uploaded documents.")
        return
    
    # Create embeddings
    embeddings = OpenAIEmbeddings()
    knowledge_base = FAISS.from_texts(texts=chunks, embedding=embeddings)

    # Show user input
    user_question = st.text_input("Ask a question about the uploaded documents:")
    if user_question:
        docs = knowledge_base.similarity_search(user_question)
        
        llm = ChatOpenAI(
            temperature=0, model="gpt-4", openai_api_key=openai_api_key, streaming=True
        )
        chain = load_qa_chain(llm, chain_type="stuff")
        with get_openai_callback() as cb:
            response = chain.run(input_documents=docs, question=user_question)
            print(response)
        
        # Display the response
        if "table" in user_question.lower() or "tabular" in user_question.lower():
            try:
                # Try to convert response to DataFrame and display
                df = pd.DataFrame(eval(response))
                st.write(df)
            except Exception as e:
                # If conversion fails, display error and text response
                #st.write(f"Error displaying table: {e}")
                st.write(response)
        else:
            st.write(response)

if __name__ == '__main__':
    app()
