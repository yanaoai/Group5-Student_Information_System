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

- Daily stand-ups
- Iterative development on feature branches
- Tests written *before* implementation
- Continuous integration via pull requests into `develop`
- Final stable build merged into `main`

---

## 3. Git Workflow

### 🔹 Main branches

| Branch    | Purpose                               |
| --------- | ------------------------------------- |
| `main`    | Stable release/demo version (protected) |
| `develop` | Main development branch (protected; all feature PRs merged here) |

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

- Have at least one code review

- Pass automated tests

- Include a clear description of changes

- Avoid direct push to main or develop

---

## 4. Branch Protection Rules (GitHub)

Settings for main and develop:

- Require pull request before merging

- Require status checks (tests) to pass

- Require linear history

- Require conversation resolution before merging

- Do not allow bypassing protection

Ensures TDD compliance and code quality.

---

## 5. Test-Driven Development (TDD)

Workflow:

- Write tests first

- Run tests → should fail (red)

- Implement minimal logic

- Run tests → pass (green)

- Refactor → keep tests green
