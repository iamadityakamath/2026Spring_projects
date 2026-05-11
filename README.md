# 2026Spring_projects
Forks from here that were made March-April 2026 are final projects from that semester.

# Does the Data Job Market Actually Reward What It Claims To? 
A Multi-Dataset Analysis of Salaries, AI Sentiment, and Remote Work

## TEAM MEMBERS:

- Aditya Kamath — [@iamadityakamath](https://github.com/iamadityakamath)
- Kritika Agrawal — [@agrawal-kritika](https://github.com/agrawal-kritika)
- Shivani — [@ShivaniB06](https://github.com/ShivaniB06)

## GITHUB REPOSITORY: https://github.com/iamadityakamath/2026Spring_projects

## How to Run

```bash
# Step 1: Create a virtual environment
python -m venv .so_venv

# Step 2: Activate the virtual environment
# macOS / Linux
source .so_venv/bin/activate

# Windows PowerShell
.so_venv\Scripts\Activate.ps1

# Step 3: Install dependencies
pip install -r requirements.txt

# Step 4: Run the project
python main.py
```

## PROJECT STRUCTURE

```
2026Spring_projects/
├── Analysis/                    # Analysis scripts for each hypothesis
│   ├── h1_analysis.py
│   ├── h2_analysis.py
│   └── h3_analysis.py
├── Data/                        # Data directory
│   ├── data_science_salaries.csv
│   └── so_surveys/             # Stack Overflow survey data by year
│       ├── 2020/
│       │   └── survey_results_public.csv
│       ├── 2021/
│       │   └── survey_results_public.csv
│       ├── 2022/
│       │   └── survey_results_public.csv
│       ├── 2023/
│       │   └── survey_results_public.csv
│       ├── 2024/
│       │   └── survey_results_public.csv
│       └── 2025/
│           └── survey_results_public.csv
├── Helper/                      # Helper modules and constants
│   ├── __init__.py
│   ├── config.py
│   ├── H1_constants.py
│   ├── H2_constants.py
│   ├── H3_constants.py
│   └── helper.py
├── Jupyter Notebook/            # Jupyter notebooks for analysis
│   ├── H1_Hypothesis/
│   │   ├── H1_Analysis.ipynb
│   │   └── H1_Preprocessing.ipynb
│   ├── H2_Hypothesis/
│   │   ├── H2_ai_satisfaction.ipynb
│   │   ├── H2_data_cleanup.py
│   │   └── download_H2_survey_files.py
│   └── H3_Hypothesis/
│       ├── H3.ipynb
│       └── README.md
├── Preprocessing/               # Preprocessing scripts for each hypothesis
│   ├── h1_preprocessing.py
│   ├── h2_preprocessing.py
│   └── h3_preprocessing.py
├── tools/                       # Utility tools
├── main.py                      # Main entry point
├── data_download.py             # Script to download datasets
├── delete_data.py               # Script to delete datasets
├── download_report.py           # Script to generate reports
├── requirements.txt             # Python dependencies
├── sample.txt                   # Sample data file
└── README.md                    # Project documentation
```

## PROJECT TYPE: 
### Type III — Original Data Analysis

### PROJECT OVERVIEW:

There is a lot of advice out there about what drives salaries and job satisfaction in the data field:
- Picking the right job title
- Adopting AI tools
- Working remotely
Most of it comes from surface-level analyses that skip real statistical checks. <br>
We want to test three of these popular claims directly using actual data and proper hypothesis testing.

## RESEARCH QUESTIONS:
Hypotheses

**H1**: Job title explains less about salary than where the company is and how senior the role is, and analyses that rank titles without these controls are misleading.

**H2**: Developers who use AI tools report higher job satisfaction, but this gap shrinks once you account for how experienced they are. We aim to analyze whether experienced people use AI search for jobs. If yes, then how beneficial is it for them? As they might have more experience themselves than AI.

**H3**: The salary advantage that remote roles had in 2020-2022 (COVID Panedamic work from home wave) has faded by 2023-2024 (when offices opened again), and analysing that pool of all five years together might produce misleading conclusions, as the data might be old. We would analyse the difference between people's salaries for work-from-home job roles from 2020-2022 and the same for remote/in-person job roles from 2023-2025.

## DATASETS: 
### We are using three datasets:

1. **Stack Overflow Developer Survey 2024**  
   - ~65,000 developers across 185 countries  
   - Includes salary, experience, AI usage, and job satisfaction  
   - 🔗 https://survey.stackoverflow.co/2024/

2. **Data Science Salaries 2024**  
   - Extends structured salary coverage  
   - Combined dataset ~23,000 records  
   - 🔗 https://www.kaggle.com/datasets/sazidthe1/data-science-salaries

These datasets come from completely different sources and cannot be merged row by row. Instead, we analyze them in parallel and use the SO Survey as an independent check on patterns we find in the salary data.

## Methodology

- Data cleaning and preprocessing across all datasets
- Parallel analysis (datasets are not merged row-wise)
- Statistical testing:
  - Regression analysis
  - Hypothesis testing
  - Controlled comparisons (experience, location, etc.)
- Cross-validation using Stack Overflow data

## Why This Matters

Most public analyses:
- Rank salaries by job title without controlling variables
- Report AI adoption rates without segmenting by experience
- Ignore time trends in remote work

We address these gaps using **statistical rigor instead of surface-level insights**.

## Use of AI

AI tools were used to help draft this README, create some helper functions, and refactor parts of the code to make them more reusable.
