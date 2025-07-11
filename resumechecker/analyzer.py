import pdfplumber
import spacy
from groq import Groq
import json
import os
from dotenv import load_dotenv

# ✅ Load environment variables from .env file
load_dotenv(
    dotenv_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
)


def extract_text_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text.strip()


def analyze_resume_with_llm(resumq_text, job_description):
    prompt = f"""
        You are an AI assistant that analyzes resumes for a software engineering job application.  
        Given a resume and a job description, extract the following details:

        1. Identify all skills mentioned in the resume.  
        2. Calculate the total years of experience.  
        3. Categorize the projects based on the domain (e.g, AI, Web development, Cloud etc)  
        4. Rank the resume relevance to the job description on a scale of 0 to 100.

        Resume:
        {resumq_text}

        Job Description:
        {job_description}

        Provide the output in valid JSON format with this structure:
        {{
            "rank" : "<percentage>",
            "skills" : ["skill1", "skill2", ......],
            "total_experience" : "<number of years>",
            "project_category" : ["category1", "category2"]
        }}
        """
    try:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        responce = client.chat.completions.create(
            model="deepseek-r1-distill-llama-70b",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            response_format={"type": "json_object"},
        )
        result = responce.choices[0].message.content
        print(result)
        return json.loads(result)  # type: ignore
    except Exception as e:
        print(f"Error: {e}")


def process_resume(pdf_path, job_description):
    try:
        resume_text = extract_text_from_pdf(pdf_path)
        data = analyze_resume_with_llm(
            resumq_text=resume_text, job_description=job_description
        )
        print(f"Data from LLM: {data}")
        return data
    except Exception as e:
        print(f"Error from process_resume: {e}")
        return None
