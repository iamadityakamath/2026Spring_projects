from Helper.config import BASE
from typing import List, Dict

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

DEFAULT_PLOTS: List[str] = [
    "h1_salary_by_title.png",
    "h1_salary_by_country.png",
    "h1_salary_by_seniority.png",
    "h1_salary_heatmap.png",
    "h1_salary_trends.png",
]

DEFAULT_HYPOTHESES: Dict[str, str] = {
    "h1_salary_by_title.png": '''H1-A: Title rankings look meaningful on the surface with Management ($120K) to Research ($50K) but the spread is largely driven by geography and seniority, not title itself. 
                                 The tight $65-70K cluster across very different mid-tier roles already hints that title alone explains little once other factors are controlled.''',
    "h1_salary_by_country.png": '''H1-B: The US dominates at $140K; nearly 2.5x Sweden or Japan. Even within high-income countries, the range is massive ($56K-$140K). This is the key evidence for H1: 
                                    A "Data/ML Engineer" in the US earns more than a "Management" role in Japan. Country alone affects title as a salary predictor, making any title-only ranking misleading without geographic controls.''',
    "h1_salary_by_seniority.png": '''H1-C: A steep progression from $35K (0-2 yrs) to $105K (20+ yrs), a 3x increase purely on experience. 
                                    This reinforces H1: seniority alone produces a larger salary spread than most title differences seen in Chart 1. A senior Back-End developer likely out-earns a junior Data/ML engineer, making title comparisons without seniority controls essentially meaningless.''',
    "h1_salary_heatmap.png": '''H1-D: The strongest evidence for H1. A Front-End developer in the US earns $121K more than a Data/ML engineer in Canada ($80K) or Germany ($75K). 
                                    India's entire row ($14-20K) sits below any single cell in the US row. Within each country, title differences are modest (US range: $105-$160K); across countries, the gap is enormous. Geography dominates title — every time.''',
    "h1_salary_trends.png": '''H1-E: All titles rose together through 2020-2023, then dipped in 2024 (likely reflecting tech layoffs and hiring freezes), before recovering in 2025. Data/ML breaks away sharply in 2025 ($105K), reflecting AI-driven demand. Crucially, the lines move in sync — macro conditions and year affect all titles similarly, reinforcing H1: external forces and timing matter more than title label. The 2024 dip hits every role equally regardless of title.''',
}

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
