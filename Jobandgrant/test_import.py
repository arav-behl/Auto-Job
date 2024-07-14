import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from backend import run_job_search
    print("Successfully imported run_job_search")
except ImportError as e:
    print(f"Failed to import run_job_search. Error: {str(e)}")
