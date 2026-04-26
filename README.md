# 2026Spring_projects
Forks from here that were made March-April 2026 are final projects from that semester.

# Does the Data Job Market Actually Reward What It Claims To? 
A Multi-Dataset Analysis of Salaries, AI Sentiment, and Remote Work

## TEAM MEMBERS:

- Aditya Kamath — [@iamadityakamath](https://github.com/iamadityakamath)
- Kritika Agrawal — [@agrawal-kritika](https://github.com/agrawal-kritika)
- Shivani Beniwal — [@ShivaniB06](https://github.com/ShivaniB06)

## GITHUB REPOSITORY: https://github.com/iamadityakamath/2026Spring_projects

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

**H3**: The salary advantage that remote roles had in 2020–2022 (COVID Panedamic work from home wave) has faded by 2023–2024 (when offices opened again), and analysing that pool of all five years together might produce misleading conclusions, as the data might be old. We would analyse the difference between people's salaries for work-from-home job roles from 2020-2022 and the same for remote/in-person job roles from 2023-2025.

## DATASETS: 
### We are using three datasets:

1. **Stack Overflow Developer Survey 2024**  
   - ~65,000 developers across 185 countries  
   - Includes salary, experience, AI usage, and job satisfaction  
   - 🔗 https://survey.stackoverflow.co/2024/

2. **Jobs in Data (ai-jobs.net)**  
   - ~9,000 salary records (2020–2024)  
   - Includes role, company size, and work setting  
   - 🔗 https://www.kaggle.com/datasets/hummaamqaasim/jobs-in-data

3. **Data Science Salaries 2024**  
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
