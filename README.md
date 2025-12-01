# Group5-Student_Information_System

---

## 1. Project Overview

The Student Information system requires a prototype system to integrate multiple sources of student wellbeing data.
This Python-based system with a relational database backend is designed to:

- **Collect weekly student data**
- Attendance
- Coursework submissions
- Wellbeing survey results (stress level, hours slept)
- **Provide simple analytics**
- Average attendance
- Stress trend visualization
- Identify problematic weeks
- **Provide CRUD operations** for authorized users
- Demonstrate feasibility of a combined wellbeing analytics system

---

## 2. SDLC Methodology

We adopted **TDD (Test-Driven Development)**:

- Write tests first
- Run tests → should fail (red)
- Implement minimal logic
- Run tests → pass (green)
- Refactor → keep tests green

---

## 3. Git Workflow

### 🔹 Main branches

| Branch     | Purpose                               |
| ---------  | ------------------------------------- |
| `main`     | Stable release/demo version (protected) |
| `develop`  | Main development branch (protected; all feature PRs merged here) |
| `feature/*`| Individual feature branches |

### 🔹 Feature Branch Strategy

Each member creates feature branches from `develop`:

```bash
git checkout develop
git pull
git checkout -b feature-<module-name>
```
Examples:
feature-database

### 🔹 Pull Request Rules

All PRs must:

- Auther Info (Student ID)

- Have at least one code review

- Pass tests

- Include a clear description of changes

- No direct push to 'main' or 'develop'

---

## 4. Branch Protection Rules

Settings for main and develop:

- Require pull request before merging

- Require status checks (tests) to pass

- Require linear history

- Do not allow bypassing protection

---

## 5. Setup & Run

```bash
git clone https://github.com/yanaoai/Group5-Student_Information_System.git
cd Group5-Student_Information_System
pip install -r requirements.txt
pytest   # run tests
python SIS_run.py   # run system
```
