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

DEFAULT_PLOTS = [
    "h3_pooled_salary_by_work_model.png",
    "h3_salary_trends_by_work_model.png",
    "h3_covid_vs_post_comparison.png",
    "h3_salary_distribution_by_era.png",
]

DEFAULT_HYPOTHESES = {
    "h3_pooled_salary_by_work_model.png": "H3-A: Pooled salary distributions across Remote, On-site, and Hybrid work models (2020-2024). Remote workers show the highest median salary, but the overlap between groups suggests work model alone is not the dominant factor once year and experience are controlled.",
    "h3_salary_trends_by_work_model.png": "H3-B: Salary trends by work model over time. All three models track macro conditions closely, rising through 2022 and softening in 2023-2024. The parallel movement indicates that year-level shocks affect all work models equally, reinforcing H3: temporal confounders must be controlled before attributing salary differences to work model.",
    "h3_covid_vs_post_comparison.png": "H3-C: COVID-era (2020-2021) vs post-COVID (2022-2024) salary comparison by work model. The Remote premium visible in the COVID era narrows significantly post-2022 as on-site and hybrid roles recovered, showing the apparent Remote advantage was partly a temporal artifact rather than a structural one.",
    "h3_salary_distribution_by_era.png": "H3-D: Salary distribution by era and work model. The spread within each work model is wide in both eras, with experience level driving more variance than work model label. This supports H3: failing to control for era and seniority leads to misleading conclusions about the effect of work model on compensation.",
}
