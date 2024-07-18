#simplified code-

import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
import os
import sys

# Append the directory where this script is located to the system path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configure the Streamlit page
st.set_page_config(page_title="AI Job Application Assistant", page_icon=":briefcase:", layout='wide')

# Load environment variables
load_dotenv()

# Attempt to import backend functionalities
try:
    from backend import run_job_search
    backend_available = True
except ImportError as e:
    backend_available = False
    st.warning(f"Job search functionality not available. Error: {str(e)}")

try:
    from resume_builder import process_job_application
    resume_builder_available = True
except ImportError as e:
    resume_builder_available = False
    st.warning(f"Resume builder functionality not available. Error: {str(e)}")

st.title("AutoJob")

# Create a sidebar for navigation
app_mode = st.sidebar.selectbox("Choose the app mode", ["Job Search", "Resume Builder"])

if app_mode == "Job Search" and backend_available:
    st.header("Job Search")
    query = st.text_input("What job are you looking for?")
    if st.button("Search") and query:
        try:
            job_search_result = run_job_search(query)
            st.write(job_search_result)
        except Exception as e:
            st.error(f"An error occurred while processing your request: {str(e)}")
    else:
        st.warning("Please enter a job search query.")

elif app_mode == "Resume Builder" and resume_builder_available:
    st.header("Resume Builder")
    job_url = st.text_input("Enter the job posting URL:")
    if st.button("Generate Application Materials") and job_url:
        with st.spinner("Processing your application..."):
            try:
                result = process_job_application(job_url)
                st.subheader("Tailored Resume")
                st.markdown(result["tailored_resume"])
                st.subheader("Interview Materials")
                st.markdown(result["interview_materials"])
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please enter a job posting URL.")
else:
    st.error("The selected functionality is not available. Please check your backend files and dependencies.")

# Function to extract text from PDF files
def get_pdf_text(docs):
    text = ""
    for pdf in docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    return text

# Main function to handle PDF uploads and text extraction
def main():
    st.sidebar.title("PDF Processing")
    docs = st.sidebar.file_uploader("Upload PDFs", accept_multiple_files=True)
    if docs:
        with st.spinner("Extracting text from PDF..."):
            extracted_text = get_pdf_text(docs)
            st.text_area("Extracted Text", extracted_text, height=300)

if __name__ == '__main__':
    main()




























# import streamlit as st
# import sys
# import os
# from dotenv import load_dotenv
# from PyPDF2 import PdfReader
# from langchain.text_splitter import CharacterTextSplitter
# from langchain.embeddings import HuggingFaceEmbeddings
# from langchain.vectorstores import FAISS
# from langchain.chains import ConversationalRetrievalChain
# from langchain.memory import ConversationBufferMemory
# from openai import OpenAI

# sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# st.set_page_config(page_title="AI Job Application Assistant", page_icon=":briefcase:", layout='wide')

# # Try importing both modules
# try:
#     from backend import run_job_search
#     backend_available = True
# except ImportError as e:
#     st.warning(f"Job search functionality not available. Error: {str(e)}")
#     backend_available = False

# try:
#     from resume_builder import process_job_application
#     resume_builder_available = True
# except ImportError as e:
#     st.warning(f"Resume builder functionality not available. Error: {str(e)}")
#     resume_builder_available = False

# st.title("AutoJob")

# # Create a sidebar for navigation
# app_mode = st.sidebar.selectbox("Choose the app mode",
#     ["Job Search", "Resume Builder"])

# if app_mode == "Job Search" and backend_available:
#     st.header("Job Search")
#     query = st.text_input("What job are you looking for?")
#     if st.button("Search"):
#         if query:
#             try:
#                 job_search_result = run_job_search(query)
#                 st.write(job_search_result)
#             except Exception as e:
#                 st.error(f"An error occurred while processing your request: {str(e)}")
#         else:
#             st.warning("Please enter a job search query.")

# elif app_mode == "Resume Builder" and resume_builder_available:
#     st.header("Resume Builder")
#     job_url = st.text_input("Enter the job posting URL:")
#     if st.button("Generate Application Materials"):
#         if job_url:
#             with st.spinner("Processing your application... This may take a few minutes."):
#                 try:
#                     result = process_job_application(job_url)

#                     st.subheader("Tailored Resume")
#                     st.markdown(result["tailored_resume"])

#                     st.subheader("Interview Materials")
#                     st.markdown(result["interview_materials"])
#                 except Exception as e:
#                     st.error(f"An error occurred: {str(e)}")
#         else:
#             st.warning("Please enter a job posting URL.")

# else:
#     st.error("The selected functionality is not available. Please check your backend files and dependencies.")

# # Load environment variables
# load_dotenv()

# # Function to extract text from PDF
# def get_pdf_text(docs):
#     text = ""
#     for pdf in docs:
#         pdf_reader = PdfReader(pdf)
#         for page in pdf_reader.pages:
#             text += page.extract_text()
#     return text

# # Split text into chunks
# def get_chunks(raw_text):
#     text_splitter = CharacterTextSplitter(separator="\n", chunk_size=1000, chunk_overlap=200)
#     chunks = text_splitter.split_text(raw_text)
#     return chunks

# # Create vector store from chunks
# def get_vectorstore(chunks):
#     embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
#     vectorstore = FAISS.from_texts(texts=chunks, embedding=embeddings)
#     return vectorstore

# def get_conversationchain(vectorstore):
#     llm = OpenAI(temperature=0.2)
#     memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True, output_key='answer')
#     conversation_chain = ConversationalRetrievalChain.from_llm(
#         llm=llm,
#         retriever=vectorstore.as_retriever(),
#         memory=memory
#     )
#     return conversation_chain

# # Main Streamlit app function
# def main():
#     st.title("AutoJob")

#     # Sidebar for PDF upload
#     with st.sidebar:
#         docs = st.file_uploader("Upload PDFs", accept_multiple_files=True)
#         if docs and st.button("Process Documents"):
#             raw_text = get_pdf_text(docs)
#             text_chunks = get_chunks(raw_text)
#             vectorstore = get_vectorstore(text_chunks)
#             st.session_state['conversation_chain'] = get_conversationchain(vectorstore)

#     # Handle chat stream
#     if "messages" not in st.session_state:
#         st.session_state.messages = []

#     for message in st.session_state.messages:
#         with st.chat_message(message["role"]):
#             st.markdown(message["content"])

#     if len(st.session_state.messages) >= 20:
#         st.info("Maximum message limit reached.")
#     else:
#         query = st.chat_input("What job are you looking for?")
#         if query:
#             st.session_state.messages.append({"role": "user", "content": query})

#             if backend_available:
#                 try:
#                     # Process the job search query using the backend
#                     job_search_result = run_job_search(query)

#                     # Display the job search result
#                     with st.chat_message("assistant"):
#                         st.markdown(job_search_result)
#                         st.session_state.messages.append({"role": "assistant", "content": job_search_result})
#                 except Exception as e:
#                     st.error(f"An error occurred while processing your request: {str(e)}")
#             else:
#                 st.error("Backend is not available. Please check your backend.py file and restart the application.")

# if __name__ == '__main__':
#     main()






# # You can keep additional features like PDF upload if needed
