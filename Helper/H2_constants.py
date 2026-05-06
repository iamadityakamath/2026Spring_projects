from Helper.config import BASE
from typing import List, Dict

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

DEFAULT_PLOTS: List[str] = [
    "H2_plot1_overall_boxplot.png",
    "H2_plot2_seniority_gap.png",
    "H2_plot3_grouped_bar.png",
]

DEFAULT_HYPOTHESES = {
    "H2_plot1_overall_boxplot.png": """Both AI users and non-AI users have a median satisfaction score of 7 out of 10. The boxes overlap almost completely, meaning the difference is small at first glance. However with 49,000+ respondents, even a small difference can be statistically real — which is why we ran formal tests rather than just eyeballing the chart.
Key takeaway: AI users are slightly happier overall, but you cannot see it clearly without statistical testing.
*/""",
    "H2_plot2_seniority_gap.png": """This chart shows how much higher AI users score compared to non-AI users within each experience group. The results surprised us:

Junior (0–2 yrs): Gap of 0.105 — marked ns (not significant). Junior developers show no real difference between AI users and non-users.
Mid-level (3–7 yrs): Gap of 0.183 — marked *** (highly significant). The gap becomes real here.
Senior (8–15 yrs): Gap of 0.217 — marked *** (highly significant). Gap grows further.
Expert (16+ yrs): Gap of 0.224 — marked *** (highly significant). Largest gap of all.

This directly contradicts our hypothesis. We expected the gap to shrink with experience — instead it grows steadily from junior to expert.
Key takeaway: The more experienced the developer, the more AI tools seem to boost their job satisfaction.""",
    "H2_plot3_grouped_bar.png": """This chart shows the actual satisfaction scores side by side for each seniority band. Two clear patterns emerge:

AI users (blue) are consistently higher than non-AI users (red) in every single band — no exceptions.
Satisfaction increases with seniority regardless of AI usage — experts are happier than juniors with or without AI tools.

The gap between blue and red bars visibly widens from left to right, visually confirming what Plot 2 showed statistically.
Key takeaway: Seniority drives satisfaction on its own, and AI tool usage adds an extra boost on top — and that boost gets stronger as developers become more experienced."""
}
