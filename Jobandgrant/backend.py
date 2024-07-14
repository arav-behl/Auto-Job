# backend.py

import os
import json
from datetime import datetime, timedelta
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
from openai import OpenAI


# Load environment variables
from dotenv import load_dotenv
load_dotenv()
openai_api_key = "api-key"
serper_api_key = "api-key"


os.environ["OPENAI_API_KEY"] = openai_api_key
os.environ["OPENAI_MODEL_NAME"] = 'gpt-4o'
os.environ["SERPER_API_KEY"] = serper_api_key

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

input_parser = Agent(
    role='Input Parsing Specialist',
    goal='Parse the user\'s input to extract job {role}, {location}, {company_type}, and {preferences}.',
    verbose=True,
    memory=False,
    backstory=(
        "You are a linguistic expert with an exceptional ability to interpret and extract key details from text inputs."
        " Your sharp understanding of language nuances allows you to parse user prompts accurately to provide clear and actionable data."
    ),
    allow_delegation=False
)

def parse_user_input(prompt):
    print(f"Received prompt: {prompt}")  # Debugging line
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an expert in extracting information from user prompts."},
            {"role": "user", "content": f"Extract the following details from the user's prompt: job role, location, company type, and any other specified preferences, including a preference for recent job postings.\n\nUser Prompt: {prompt}\n\nExpected Output: A JSON object with the following keys: role, location, company_type, preferences.\nExample Output: {{'role': 'Data Analyst', 'location': 'Bengaluru', 'company_type': 'Fintech', 'preferences': {{'experience': '5 years', 'date_range': 'last 30 days'}}}}"}
        ]
    )
    output = response.choices[0].message.content.strip()
    print(f"Parsed output: {output}")  # Debugging line

    if output.startswith("```") and output.endswith("```"):
        output = output.strip("```").strip("json").strip()

    output = output.replace('null', 'None')
    return json.loads(output)  # Safely parse the JSON output

parsing_task = Task(
    description=(
        "Parse the user's prompt to extract the job {role}, {location}, {company_type}, and any other specified {preferences}."
        " Ensure that the extracted information is clear and formatted appropriately for further processing."
    ),
    expected_output='A dictionary with keys: role, location, company_type, and preferences.',
    agent=input_parser,
    run_function=lambda inputs: parse_user_input(inputs['user_prompt'])  # Ensure the function uses the correct input
)

job_researcher = Agent(
    role='Senior Job Researcher',
    goal='Identify and compile a list of job postings that match the user\'s specific criteria.',
    verbose=True,
    memory=True,
    backstory=(
        "You have spent years in the field of recruitment, specializing in finding the best job opportunities for clients."
        " Your expertise lies in navigating various job boards, company websites, and social media to uncover hidden gems in the job market."
        " Your dedication and sharp eye for detail ensure that you never miss a relevant job posting."
    ),
    tools=[SerperDevTool()],
    allow_delegation=True
)

def search_for_jobs(parsed_data):
    role = parsed_data.get('role')
    location = parsed_data.get('location')
    company_type = parsed_data.get('company_type')
    preferences = parsed_data.get('preferences')
    date_range = preferences.get('date_range', 'last 30 days')
    print(f"Searching for jobs with role: {role}, location: {location}, company_type: {company_type}, preferences: {preferences}")  # Debugging line

    job_list = [
        {'title': 'Data Analyst', 'company': 'Fintech XYZ', 'location': 'Bengaluru', 'description': 'Exciting opportunity in a fintech company.', 'date_posted': '2024-07-01'},
        {'title': 'Product Manager', 'company': 'Tech ABC', 'location': 'Bengaluru', 'description': 'Great opportunity in a tech company.', 'date_posted': '2023-12-15'},
    ]

    cutoff_date = datetime.now() - timedelta(days=int(date_range.split()[1]))
    filtered_jobs = [job for job in job_list if datetime.strptime(job['date_posted'], '%Y-%m-%d') >= cutoff_date]
    return filtered_jobs

job_search_task = Task(
    description=(
        "Using the parsed criteria from the user's prompt, search for job postings that match the specified job title, company type, and location."
        " Ensure the job postings are recent and still accepting applications."
    ),
    expected_output='A list of job postings that match the criteria, including job title, company name, location, and a brief job description.',
    agent=job_researcher,
    run_function=lambda inputs: search_for_jobs(inputs)  # Use the parsed data
)

job_analyst = Agent(
    role='Expert Job Analyst',
    goal='Evaluate and filter job postings to ensure they meet the criteria specified by the user.',
    verbose=True,
    memory=True,
    backstory=(
        "With a background in data analysis and a passion for startups, you excel at discerning which job postings truly offer growth opportunities."
        " Your analytical skills and understanding of the startup ecosystem allow you to sift through numerous postings and identify the most promising positions."
        " You take pride in helping clients find jobs that align with their career goals and aspirations."
    ),
    allow_delegation=False
)

def analyze_jobs(job_list):
    print(f"Analyzing jobs: {job_list}")  # Debugging line
    return job_list

job_analysis_task = Task(
    description=(
        "Analyze the list of job postings provided by the Job Researcher."
    ),
    expected_output='A refined list of job postings that fit the specified criteria, including detailed analysis of each posting with clickable links.',
    agent=job_analyst,
    run_function=lambda inputs: analyze_jobs(inputs['job_list'])  # Use the job list
)

job_search_crew = Crew(
    agents=[input_parser, job_researcher, job_analyst],
    tasks=[parsing_task, job_search_task, job_analysis_task],
    process=Process.sequential  # Sequential process
)


def run_job_search(user_prompt):
    try:
        parsed_result = parse_user_input(user_prompt)
        print(f"Parsed Result: {parsed_result}")  # Debugging line
        print(type(parsed_result))

        result = job_search_crew.kickoff(inputs=parsed_result)
        return result
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return f"An error occurred while processing your request: {str(e)}"

# Test the function if this file is run directly
if __name__ == "__main__":
    test_prompt = "AI engineer roles in a genAI startup in Bangalore in the past 7 days"
    result = run_job_search(test_prompt)
    print(result)
