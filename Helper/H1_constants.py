BASE = "/Users/aditya/Documents/PR/PR FInal Project/2026Spring_projects/Data"

YEAR_FILES = {
    yr: f"{BASE}/so_surveys/{yr}/survey_results_public.csv"
    for yr in range(2020, 2026)
}

FINAL_COLS = [
    "ResponseId", "MainBranch", "Employment", "Country",
    "DevType", "OrgSize", "YearsCode", "YearsCodePro",
    "WorkExp", "ICorPM", "ConvertedCompYearly"
]

COLUMN_OVERRIDES = {
    2020: {"ResponseId": "Respondent", "ConvertedCompYearly": "ConvertedComp", "WorkExp": None, "ICorPM": None},
    2021: {"WorkExp": None, "ICorPM": None},
    2025: {"YearsCodePro": None}
}

KEEP_EMPLOYMENT = {
    "Employed, full-time",
    "Employed full-time",
    "Independent contractor, freelancer, or self-employed",
    "Self-employed",
    "Employed part-time",
    "Employed, part-time"
}

SALARY_LOW  = 5_000
SALARY_HIGH = 500_000

DEV_CATEGORY_MAP = {
    "Developer, full-stack":"Full-Stack",
    "Developer, back-end":"Back-End",
    "Developer, front-end":"Front-End",
    "Developer, mobile":"Mobile",
    "Data scientist or machine learning specialist":"Data/ML",
    "Data or business analyst":"Data/ML",
    "Engineer, data":"Data/ML",
    "DevOps specialist":"DevOps/Cloud",
    "Engineer, site reliability":"DevOps/Cloud",
    "Cloud infrastructure engineer":"DevOps/Cloud",
    "Developer, embedded applications or devices":"Embedded/Systems",
    "Engineer, embedded systems":"Embedded/Systems",
    "Security professional":"Security",
    "Developer, QA or test":"QA/Test",
    "Product manager":"Management",
    "Engineering manager":"Management",
    "Senior Executive (C-Suite, VP, etc.)":"Management",
    "Developer, desktop or enterprise applications":"Desktop/Enterprise",
    "Academic researcher":"Research/Academia",
    "Scientist":"Research/Academia"
}

ORG_SIZE_MAP = {
    "Just me - I am a freelancer, sole proprietor, etc.":1,
    "2 to 9 employees":2,
    "10 to 19 employees":3,
    "Less than 20 employees":3,
    "20 to 99 employees":4,
    "100 to 499 employees":5,
    "500 to 999 employees":6,
    "1,000 to 4,999 employees":7,
    "5,000 to 9,999 employees":8,
    "10,000 or more employees":9,
    "I don't know":None
}

PLOTS_DIR = "Data/Analysis Plots/H1_Analysis"

COUNTRY_SHORT = {
    'United States of America': 'USA',
    'United Kingdom of Great Britain and Northern Ireland': 'UK',
    'Germany': 'Germany',
    'India': 'India',
    'Canada': 'Canada',
    'France': 'France',
    'Brazil': 'Brazil',
    'Australia': 'Australia',
    'Netherlands': 'Netherlands',
    'Poland': 'Poland',
}

TIER1 = {
    "United States", "United States of America", "Switzerland",
    "Australia", "Canada", "Israel", "Denmark", "Norway",
    "Netherlands", "Singapore", "Luxembourg"
}
TIER2 = {
    "United Kingdom", "United Kingdom of Great Britain and Northern Ireland",
    "Germany", "Ireland", "Sweden", "Finland", "Austria", "France",
    "New Zealand", "United Arab Emirates", "Japan", "Iceland", "Belgium"
}
TIER3 = {
    "Spain", "Italy", "Portugal", "Czech Republic", "Poland", "Hungary",
    "Romania", "Estonia", "Slovenia", "Slovakia", "Lithuania", "Latvia",
    "Greece", "Turkey", "Cyprus", "Malta", "Croatia", "Serbia", "Bulgaria",
    "Ukraine", "Russian Federation", "Kazakhstan", "China", "South Korea",
    "Republic of Korea", "Taiwan", "Malaysia", "Thailand", "Chile", "Mexico",
    "Brazil", "Argentina", "Costa Rica", "Panama", "Uruguay", "South Africa",
    "Saudi Arabia", "Qatar", "Kuwait"
}
