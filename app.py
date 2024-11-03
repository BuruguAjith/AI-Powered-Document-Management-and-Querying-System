import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Google API key
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(api_key=api_key, model="models/embedding-001")
    
    if len(text_chunks) == 0:
        raise ValueError("No text chunks provided for vector store creation.")
    
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")

def get_conversational_chain():
    prompt_template = """
    Answer the question as detailed as possible from the provided context, 
    make sure to provide all the details. If the answer is not in the provided context, just say,
    "answer is not available in the context". Don't provide the wrong answer.\n\n
    Context:\n {context}?\n
    Question:\n {question}\n

    Answer:
    """

    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain

def user_input(user_question):
    try:
        # Initialize embeddings with required parameters
        embeddings = GoogleGenerativeAIEmbeddings(api_key=api_key, model="models/embedding-001")  

        # Load the FAISS index with dangerous deserialization flag set to True
        new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)

        # Perform similarity search and retrieve documents
        docs = new_db.similarity_search(user_question)

        # Get the conversational chain
        chain = get_conversational_chain()

        # Generate the response
        response = chain({"input_documents": docs, "question": user_question}, return_only_outputs=True)

        st.write("Reply: ", response["output_text"])
    except Exception as e:
        st.error(f"An error occurred: {e}")

def main():
    st.set_page_config(page_title="AI Planet", page_icon="🌌")  # Set the title and icon

    # Set the input label with larger font size
    st.markdown("<h3 style='font-size: 25px;'>Please ask your question to AI Planet 🌍 </h3>", unsafe_allow_html=True)
    user_question = st.text_input(" ")

    with st.sidebar:
        st.title("Menu:")
        pdf_docs = st.file_uploader("Upload your PDF Files and Click on the Submit & Process Button", accept_multiple_files=True)
        if st.button("Submit & Process"):
            if pdf_docs:
                with st.spinner("Processing..."):
                    raw_text = get_pdf_text(pdf_docs)
                    if not raw_text:
                        st.error("No text extracted from the PDF files. Please check the files.")
                        return

                    text_chunks = get_text_chunks(raw_text)
                    if not text_chunks:
                        st.error("No text chunks created from the PDF content.")
                        return

                    get_vector_store(text_chunks)
                    st.success("Done")
            else:
                st.warning("Please upload at least one PDF file.")
    
    if user_question:
        user_input(user_question)

if __name__ == "__main__":
    main()
