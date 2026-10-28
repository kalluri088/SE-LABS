# Lab 4: CI/CD Pipeline Automation

Software Engineering (UE22CS341AA) — PES University  
Student: Kalluri Yaswanth (PES2UG24CS212)

## Overview

Demonstration of automated testing and deployment using GitHub Actions and GitHub Pages.

- **Application (`app.py`):** Arithmetic utilities generating an HTML page.
- **Automated Tests (`test_app.py`):** Pytest test cases for functional verification.
- **Site Artifact (`site/index.html`):** Generated deployment artifact.
- **CI/CD Workflow (`.github/workflows/pipeline.yml`):** Multi-stage automated pipeline (Test stage + Pages deploy stage).
  > **Note:** The workflow file is maintained within this subdirectory as reference documentation from the original standalone repository [`kalluri088/SE-CICD-LAB`](https://github.com/kalluri088/SE-CICD-LAB) so as not to trigger unverified repository-level Actions on `SE-LABS`.
- **Evidence Report (`CICD Demo.pdf`):** Execution logs and deployment confirmation.
