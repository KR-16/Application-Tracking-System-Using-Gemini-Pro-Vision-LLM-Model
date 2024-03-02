from dotenv import load_dotenv
import streamlit as st
import base64
import os
import io
from PIL import Image
import pdf2image
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def getResponse(input, pdf_content, prompt):
    model = genai.GenerativeModel("gemini-pro-vision")
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

def inputPDFsetup(upload_file):
    """
    PDF2IMAGE convert the image into bytes
    """

    if upload_file is not None:
        images = pdf2image.convert_from_bytes(upload_file.read())

        firstPage = images[0]

        # """
        # Convert to bytes
        # """

        imageBytesArray = io.BytesIO()
        firstPage.save(imageBytesArray, format="JPEG")
        imageBytesArray = imageBytesArray.getvalue()

        pdf_parts = [
            {
                "mime_type":"image/jpeg",
                "data":base64.b64encode(imageBytesArray).decode() # encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("Need to Upload a PDF File")
    

# """
# STREAMLIT Application
# """

st.set_page_config(page_title="ATS")
st.header("YOUR RESUME EXPERT")
input_text = st.text_area("Job Description: ", key="input")
upload_file = st.file_uploader("Upload Your Resume(PDF)----", type=["pdf"])

if upload_file is not None:
    st.write("File Received Successfully")


Question1 = st.button("Tell me About my Resume")
Question2 = st.button("How can I Improvise my skills")
Question3 = st.button("Percentage Match")

input_prompt1 = """
You are an experienced Technical Human Resource Manager in the field of 
Data Science, Full Stack, Devops, Cloud, Software Engineer, Machine Learning Engineering, Data Analyst 
your task is to review the provided resume against the Job Description for these profiles.
Please share your professional evaluation on whether the candidate's profile aligns with the role.
Highlight the strengths and weaknesses of the application in relation with the specified job requirements.
"""

input_prompt2 = """
You are an experienced Technical Human Resource Manager in the field of 
Data Science, Full Stack, Devops, Cloud, Software Engineer, Machine Learning Engineering, Data Analyst 
your role is to scrutinize the resume against the Job Description for these profiles.
Please share your professional insights on candidate's suitability for the role.
Additionally, offer advice on enhancing the candidate's skills and identify the areas where the candidate can be improved.
"""

input_prompt3 = """
You are an skilled ATS(APPLICATION TRACKING SYSTEM) scanner with a deep understanding in the field of 
Data Science, Full Stack, Devops, Cloud, Software Engineer, Machine Learning Engineering, Data Analyst 
and deep ATS funcationality.
You  task is to evaluate the resume against the provided Job Description.
Give me the percentage of the resume matches the Job Description.
First output the percentage and then the missing keywords and last final thoughts.
"""

if Question1:
    if upload_file is not None:
        pdf_content = inputPDFsetup(upload_file)
        response = getResponse(input_prompt1, pdf_content, input_text)
        st.subheader("The Response is: ")
        st.write(response)
    else:
        st.write("Upload the Resume")

elif Question2:
    if upload_file is not None:
        pdf_content = inputPDFsetup(upload_file)
        response = getResponse(input_prompt2, pdf_content, input_text)
        st.subheader("The Response is: ")
        st.write(response)
    else:
        st.write("Upload the Resume")

elif Question3:
    if upload_file is not None:
        pdf_content = inputPDFsetup(upload_file)
        response = getResponse(input_prompt3, pdf_content, input_text)
        st.subheader("The Response is: ")
        st.write(response)
    else:
        st.write("Upload the Resume")