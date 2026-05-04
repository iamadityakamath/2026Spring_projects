from Helper.config import BASE

DATA_FILE = f"{BASE}/data_science_salaries.csv"

ALL_COLS = [
    'job_title', 'experience_level', 'employment_type', 'work_models',
    'work_year', 'employee_residence', 'salary', 'salary_currency',
    'salary_in_usd', 'company_location', 'company_size',
]

YEAR_MIN = 2020
YEAR_MAX = 2024

WORK_MODELS = ['Remote', 'On-site', 'Hybrid']

PLOTS_DIR = "Data/Analysis Plots/H3_Analysis"
