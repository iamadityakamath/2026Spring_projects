BASE = "/Users/aditya/Documents/PR/PR FInal Project/2026Spring_projects/Data"

YEAR_FILES = {
    yr: f"{BASE}/so_surveys/{yr}/survey_results_public.csv"
    for yr in [2023, 2024, 2025]
}

ALL_COLS = [
    'year',
    'YearsCodePro', 'DevType', 'EdLevel', 'Employment',
    'Country', 'OrgSize',
    'ConvertedCompYearly',
    'RemoteWork',
    'AISelect', 'AISent', 'AIBen', 'AIToolCurrently Using',
    'JobSat',
]

# 2025 renames WorkExp → YearsCodePro; AIBen dropped; AI tool columns split
COLUMN_OVERRIDES_2025 = {
    'WorkExp': 'YearsCodePro',
}

SALARY_LOW  = 10_000
SALARY_HIGH = 1_000_000

SENIORITY_BANDS = [
    (2,  'Junior (0-2 yrs)'),
    (7,  'Mid-level (3-7 yrs)'),
    (15, 'Senior (8-15 yrs)'),
    (float('inf'), 'Expert (16+ yrs)'),
]

EMPLOYMENT_MAP = {
    'Employed, full-time':                                       'Full-time',
    'Independent contractor, freelancer, or self-employed':     'Freelancer/Contractor',
}

AI_FREQUENCY_MAP = {
    'daily':   'Daily',
    'weekly':  'Weekly',
    'monthly': 'Monthly/Infrequently',
}

REMOTE_MAP = {
    'remote':    'Remote',
    'in-person': 'In-person',
    'hybrid':    'Hybrid',
    'choice':    'Hybrid',
    'flexible':  'Hybrid',
}

PLOTS_DIR = "Data/Analysis Plots/H2_Analysis"
