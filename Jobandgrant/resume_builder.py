# newer code for resume_builder 

import os
import warnings
import tempfile
from pathlib import Path
from PyPDF2 import PdfReader
import markdown
from crewai import Agent, Task, Crew
from crewai_tools import FileReadTool, ScrapeWebsiteTool, SerperDevTool, MDXSearchTool

warnings.filterwarnings('ignore')

# API keys and environment setup
openai_api_key = "apikey"
serper_api_key = "apikey"
os.environ["OPENAI_API_KEY"] = openai_api_key
os.environ["OPENAI_MODEL_NAME"] = 'gpt-4'
os.environ["SERPER_API_KEY"] = serper_api_key

def pdf_to_markdown(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n\n"
    return markdown.markdown(text)

def process_resume(pdf_path, job_description):
    # Convert PDF to markdown
    md_content = pdf_to_markdown(pdf_path)
    
    # Save markdown content to a temporary file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.md') as temp_file:
        temp_file.write(md_content)
        temp_file_path = temp_file.name

    # Initialize tools
    search_tool = SerperDevTool()
    scrape_tool = ScrapeWebsiteTool()
    read_resume = FileReadTool(file_path=temp_file_path)
    semantic_search_resume = MDXSearchTool(mdx=temp_file_path)

    # Agent 1: Researcher
    researcher = Agent(
        role="Tech Job Researcher",
        goal="Make sure to do amazing analysis on job posting to help job applicants",
        tools=[scrape_tool, search_tool],
        verbose=True,
        backstory=(
            "As a Job Researcher, your prowess in navigating and extracting critical "
            "information from job postings is unmatched. Your skills help pinpoint the necessary "
            "qualifications and skills sought by employers, forming the foundation for "
            "effective application tailoring."
        )
    )

    # Agent 2: Profiler
    profiler = Agent(
        role="Personal Profiler for Engineers",
        goal="Do incredible research on job applicants to help them stand out in the job market",
        tools=[scrape_tool, search_tool, read_resume, semantic_search_resume],
        verbose=True,
        backstory=(
            "Equipped with analytical prowess, you dissect and synthesize information "
            "from diverse sources to craft comprehensive personal and professional profiles, laying the "
            "groundwork for personalized resume enhancements."
        )
    )

    # Agent 3: Resume Strategist
    resume_strategist = Agent(
        role="Resume Strategist for Engineers",
        goal="Find all the best ways to make a resume stand out in the job market.",
        tools=[scrape_tool, search_tool, read_resume, semantic_search_resume],
        verbose=True,
        backstory=(
            "With a strategic mind and an eye for detail, you excel at refining resumes to highlight the most "
            "relevant skills and experiences, ensuring they resonate perfectly with the job's requirements."
        )
    )

    # Agent 4: Interview Preparer
    interview_preparer = Agent(
        role="Engineering Interview Preparer",
        goal="Create interview questions and talking points based on the resume and job requirements",
        tools=[scrape_tool, search_tool, read_resume, semantic_search_resume],
        verbose=True,
        backstory=(
            "Your role is crucial in anticipating the dynamics of interviews. With your ability to formulate key questions "
            "and talking points, you prepare candidates for success, ensuring they can confidently address all aspects of the "
            "job they are applying for."
        )
    )

    # Define tasks
    research_task = Task(
        description=f"Research the job market and analyze the following job description: {job_description}",
        agent=researcher
    )

    profile_task = Task(
        description="Create a comprehensive profile of the job applicant based on their resume",
        agent=profiler
    )

    strategy_task = Task(
        description="Develop a strategy to tailor the resume for the specific job, highlighting relevant skills and experiences",
        agent=resume_strategist
    )

    interview_prep_task = Task(
        description="Prepare potential interview questions and talking points based on the resume and job requirements",
        agent=interview_preparer
    )

    # Create the crew
    resume_crew = Crew(
        agents=[researcher, profiler, resume_strategist, interview_preparer],
        tasks=[research_task, profile_task, strategy_task, interview_prep_task],
        verbose=2  # You can adjust this for more or less verbose output
    )

    # Execute the crew's tasks
    result = resume_crew.kickoff()

    # Clean up the temporary file
    os.unlink(temp_file_path)

    # Return the results
    return {
        "job_market_analysis": result[0],
        "applicant_profile": result[1],
        "resume_tailoring_strategy": result[2],
        "interview_prep": result[3]
    }

# Example usage
# def main():
#     pdf_path = "path/to/your/resume.pdf"
#     job_description = "Software Engineer with 3+ years of experience in Python and web development..."
#     results = process_resume(pdf_path, job_description)
#     
#     print("Job Market Analysis:", results["job_market_analysis"])
#     print("Applicant Profile:", results["applicant_profile"])
#     print("Resume Tailoring Strategy:", results["resume_tailoring_strategy"])
#     print("Interview Prep:", results["interview_prep"])
#
# if __name__ == "__main__":
#     main()






# # resume_builder.py

# import os
# import warnings
# warnings.filterwarnings('ignore')

# from crewai import Agent, Task, Crew
# from crewai_tools import FileReadTool, ScrapeWebsiteTool, SerperDevTool, MDXSearchTool

# # API keys and environment setup
# openai_api_key = "apikey"
# serper_api_key = "apikey"

# os.environ["OPENAI_API_KEY"] = openai_api_key
# os.environ["OPENAI_MODEL_NAME"] = 'gpt-4o'
# os.environ["SERPER_API_KEY"] = serper_api_key

# # Assume the resume file is in the same directory
# resume_file_path = "resume.md"  # or whatever your resume file is named

# # Initialize tools
# search_tool = SerperDevTool()
# scrape_tool = ScrapeWebsiteTool()
# read_resume = FileReadTool(file_path=resume_file_path)
# semantic_search_resume = MDXSearchTool(mdx=resume_file_path)


# # Agent 1: Researcher
# researcher = Agent(
#     role="Tech Job Researcher",
#     goal="Make sure to do amazing analysis on "
#          "job posting to help job applicants",
#     tools = [scrape_tool, search_tool],
#     verbose=True,
#     backstory=(
#         "As a Job Researcher, your prowess in "
#         "navigating and extracting critical "
#         "information from job postings is unmatched."
#         "Your skills help pinpoint the necessary "
#         "qualifications and skills sought "
#         "by employers, forming the foundation for "
#         "effective application tailoring."
#     )
# )

# # Agent 2: Profiler
# profiler = Agent(
#     role="Personal Profiler for Engineers",
#     goal="Do increditble research on job applicants "
#          "to help them stand out in the job market",
#     tools = [scrape_tool, search_tool,
#              read_resume, semantic_search_resume],
#     verbose=True,
#     backstory=(
#         "Equipped with analytical prowess, you dissect "
#         "and synthesize information "
#         "from diverse sources to craft comprehensive "
#         "personal and professional profiles, laying the "
#         "groundwork for personalized resume enhancements."
#     )
# )

# # Agent 3: Resume Strategist
# resume_strategist = Agent(
#     role="Resume Strategist for Engineers",
#     goal="Find all the best ways to make a "
#          "resume stand out in the job market.",
#     tools = [scrape_tool, search_tool,
#              read_resume, semantic_search_resume],
#     verbose=True,
#     backstory=(
#         "With a strategic mind and an eye for detail, you "
#         "excel at refining resumes to highlight the most "
#         "relevant skills and experiences, ensuring they "
#         "resonate perfectly with the job's requirements."
#     )
# )

# # Agent 4: Interview Preparer
# interview_preparer = Agent(
#     role="Engineering Interview Preparer",
#     goal="Create interview questions and talking points "
#          "based on the resume and job requirements",
#     tools = [scrape_tool, search_tool,
#              read_resume, semantic_search_resume],
#     verbose=True,
#     backstory=(
#         "Your role is crucial in anticipating the dynamics of "
#         "interviews. With your ability to formulate key questions "
#         "and talking points, you prepare candidates for success, "
#         "ensuring they can confidently address all aspects of the "
#         "job they are applying for."
#     )
# )
