# Dron AI ? Complete Parameters & UI Features Master Catalog

> **Reference Document**: This catalog provides a complete, exhaustive breakdown of **Every Single Parameter** (mathematical, database, API, ML model, environment) and **Every Single UI Feature** (screens, widgets, cards, inputs, buttons, visualizations) in the **Dron AI** platform.

---

# PART 1: COMPLETE PARAMETERS CATALOG

## 1. The 13-Dimensional ML Feature Vector

The predictive and recommendation core of Dron AI relies on an ordered 13-dimensional numerical feature vector:

$$\mathbf{X} = [x_0, x_1, x_2, \dots, x_{12}]$$

| Index | Technical Key | Data Type | Physical Range | Bounds Clamped | Default | Source | Semantic Meaning |
|:---:|:---|:---:|:---:|:---:|:---:|:---|:---|
| **0** | `cgpa` | `float` | 0.0 ? 10.0 | `[0.0, 10.0]` | `0.0` | `academic_history.cgpa` | Cumulative Grade Point Average across all completed university semesters. |
| **1** | `attendance_pct` | `float` | 0.0 ? 100.0 | `[0.0, 100.0]` | `0.0` | `academic_history.attendance_pct` | Overall class and laboratory attendance percentage. |
| **2** | `active_backlogs` | `int` | 0 ? 20+ | `[0, None]` | `0` | `academic_history.active_backlogs` | Count of currently unresolved subject failures / backlogs. |
| **3** | `dsa_score` | `float` | 0.0 ? 100.0 | `[0.0, 100.0]` | `0.0` | `skill_vectors.dsa_score` | Data Structures & Algorithms proficiency (self-assessed & verified). |
| **4** | `python_prof` | `float` | 0.0 ? 100.0 | `[0.0, 100.0]` | `0.0` | `skill_vectors.python_prof` | Python programming proficiency score. |
| **5** | `cpp_prof` | `float` | 0.0 ? 100.0 | `[0.0, 100.0]` | `0.0` | `skill_vectors.cpp_prof` | C++ programming & STL proficiency score. |
| **6** | `aiml_knowledge` | `float` | 0.0 ? 100.0 | `[0.0, 100.0]` | `0.0` | `skill_vectors.aiml_knowledge` | Machine Learning, Deep Learning, and AI conceptual score. |
| **7** | `total_commits` | `int` | 0 ? 5000+ | `[0, None]` | `0` | `github_fetcher` / `skill_vectors` | Total public GitHub commit count across all repositories in past year. |
| **8** | `problems_solved` | `int` | 0 ? 3000+ | `[0, None]` | `0` | `leetcode_fetcher` / `skill_vectors` | Total distinct coding problems solved on LeetCode (Easy + Medium + Hard). |
| **9** | `contest_rating` | `float` | 0.0 ? 3500.0 | `[0.0, None]` | `0.0` | `leetcode_fetcher` / `skill_vectors` | Official LeetCode contest rating (defaults to 0.0 if unrated). |
| **10** | `project_count` | `int` | 0 ? 50+ | `[0, None]` | `0` | `skill_vectors.project_count` | Number of verified software development / capstone projects completed. |
| **11** | `communication_score` | `float` | 0.0 ? 100.0 | `[0.0, 100.0]` | `0.0` | `skill_vectors.communication_score` | Soft skills, verbal communication, and interview demeanor rating. |
| **12** | `internship_exp` | `int` | 0 ? 48 | `[0, None]` | `0` | `skill_vectors.internship_exp` | Cumulative technical internship and work experience duration in months. |

---

## 2. Database Schema Parameters (SQLAlchemy Entities)

### Table 1: `users_master`
*Primary identity and authentication table.*
- `student_id` (`Integer`, PK, Auto-increment): Unique numerical identifier for each student.
- `full_name` (`String(150)`, Not Null): Student's full registered name.
- `email` (`String(255)`, Not Null, Unique, Indexed): University or personal email used for authentication.
- `password_hash` (`String(255)`, Not Null): Cryptographically hashed password (Argon2 / SHA-256). Never returned in API responses.
- `cohort_year` (`Integer`, Nullable): Student's expected graduation year (e.g. `2026`).
- `academic_branch` (`String(100)`, Nullable): Academic department (e.g., `Computer Science & Engineering`).
- `created_at` (`DateTime`, Default `utcnow`): Account creation timestamp.
- `updated_at` (`DateTime`, Default `utcnow`, OnUpdate `utcnow`): Last profile modification timestamp.

### Table 2: `academic_history`
*Semester-by-semester academic progression records.*
- `record_id` (`Integer`, PK, Auto-increment): Unique primary key for each academic entry.
- `student_id` (`Integer`, FK `users_master.student_id`, Not Null, Indexed, OnDelete `CASCADE`): Associated student.
- `semester` (`Integer`, Not Null): Semester number (1 to 8).
- `cgpa` (`Float`, Not Null): Cumulative Grade Point Average for that semester (0.0 to 10.0).
- `attendance_pct` (`Float`, Default `0.0`): Class attendance percentage (0.0 to 100.0).
- `active_backlogs` (`Integer`, Default `0`): Unresolved failed courses during that semester.
- `created_at` (`DateTime`, Default `utcnow`): Record creation timestamp.
- *Table Constraint*: `UniqueConstraint('student_id', 'semester')` ? prevents duplicate entries for the same semester.

### Table 3: `platform_links`
*External developer platform handles used for live data synchronization.*
- `link_id` (`Integer`, PK, Auto-increment): Primary key.
- `student_id` (`Integer`, FK `users_master.student_id`, Not Null, Unique, OnDelete `CASCADE`): Strictly enforces 1-to-1 relationship with `users_master`.
- `github_username` (`String(255)`, Nullable): GitHub profile username.
- `leetcode_username` (`String(255)`, Nullable): LeetCode profile username.
- `linkedin_url` (`String(500)`, Nullable): LinkedIn public profile URL.
- `last_synced` (`DateTime`, Nullable): Timestamp of the last successful live external API fetch.

### Table 4: `skill_vectors`
*Quantitative 10-dimensional skill metrics. Uses Shared PK/FK pattern.*
- `student_id` (`Integer`, PK & FK `users_master.student_id`, OnDelete `CASCADE`): Shared PK/FK enforces strict 1:1 extension without duplicate overhead.
- `dsa_score` (`Float`, Default `0.0`): Data Structures & Algorithms proficiency (0.0?100.0).
- `python_prof` (`Float`, Default `0.0`): Python proficiency (0.0?100.0).
- `cpp_prof` (`Float`, Default `0.0`): C++ proficiency (0.0?100.0).
- `aiml_knowledge` (`Float`, Default `0.0`): AI/ML conceptual knowledge (0.0?100.0).
- `total_commits` (`Integer`, Default `0`): Synced GitHub commit count.
- `problems_solved` (`Integer`, Default `0`): Synced LeetCode problem count.
- `contest_rating` (`Float`, Default `0.0`): Synced LeetCode contest rating.
- `project_count` (`Integer`, Default `0`): Self-reported project count.
- `communication_score` (`Float`, Default `0.0`): Soft skills rating (0.0?100.0).
- `internship_exp` (`Integer`, Default `0`): Internship duration in months.
- `updated_at` (`DateTime`, Default `utcnow`, OnUpdate `utcnow`): Last modification timestamp.

### Table 5: `ml_predictions`
*Audit log and cache of inference results.*
- `prediction_id` (`Integer`, PK, Auto-increment): Unique prediction transaction ID.
- `student_id` (`Integer`, FK `users_master.student_id`, Not Null, Indexed, OnDelete `CASCADE`): Associated student.
- `placement_probability` (`Float`, Nullable): Computed placement probability score ($0.0 \le P \le 1.0$).
- `readiness_tier` (`String(50)`, Nullable): Human-readable readiness classification.
- `feature_importance` (`Text`, Nullable): Serialized JSON mapping feature names to SHAP importance weights.
- `career_matches_json` (`Text`, Nullable): Serialized JSON array of cosine-similarity ranked career matches.
- `target_career_path` (`String(200)`, Nullable): Target career role selected by student.
- `roadmap_json` (`Text`, Nullable): Serialized JSON containing structured phases, tasks, and timelines.
- `created_at` (`DateTime`, Default `utcnow`, Not Null): Prediction creation timestamp.

---

## 3. Machine Learning Model Hyperparameters & Thresholds

### 3.1 XGBoost Classifier Parameters
- **Algorithm**: `xgboost.XGBClassifier`
- **Objective**: `binary:logistic`
- **Number of Estimators (`n_estimators`)**: `100`
- **Maximum Tree Depth (`max_depth`)**: `4`
- **Learning Rate (`learning_rate` / `eta`)**: `0.1`
- **Subsample Ratio (`subsample`)**: `0.8`
- **Column Sample Ratio (`colsample_bytree`)**: `0.8`
- **Evaluation Metric (`eval_metric`)**: `logloss`
- **Random State (`random_state`)**: `42`
- **Inference Time SLA**: $< 5	ext{ms}$ (Typical $< 2	ext{ms}$)

### 3.2 Placement Readiness Tier Thresholds
| Probability Range | Readiness Tier | UI Badge Color | Guidance Meaning |
|:---:|:---|:---:|:---|
| $P \ge 0.80$ | **Highly Prepared** | Emerald Green (`var(--status-success)`) | Tier-1 product company readiness; strong algorithmic & project track record. |
| $0.60 \le P < 0.80$ | **Prepared** | Neon Cyan (`var(--accent-cyan)`) | Tier-2 IT & product company ready; minor gaps in advanced algorithms or system design. |
| $0.40 \le P < 0.60$ | **Needs Improvement** | Amber Warning (`var(--status-warning)`) | Vulnerable to campus elimination rounds; active remediation required. |
| $P < 0.40$ | **High Risk / Action Required** | Rose Red (`var(--status-danger)`) | Critical deficiencies in DSA, academics, or backlogs; intensive sprint mandated. |

### 3.3 Target Career Benchmark Vectors (10-Dimensional)
The 7 predefined career vectors in `ml_engine/data/career_vectors.json`:

| Feature Dimension | Software Engineer | Data Analyst | ML Engineer | Web Developer | DevOps Engineer | Cloud Architect | Cybersecurity Analyst |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `dsa_score` | **90** | 50 | 75 | 55 | 50 | 45 | **80** |
| `python_prof` | 80 | **85** | **90** | 70 | 75 | 70 | 75 |
| `cpp_prof` | 70 | 30 | 60 | 30 | 40 | 35 | **85** |
| `aiml_knowledge` | 40 | 70 | **95** | 20 | 30 | 35 | 45 |
| `total_commits` | **85** | 50 | 70 | **90** | **90** | 65 | 60 |
| `problems_solved` | **80** | 40 | 60 | 45 | 40 | 35 | 70 |
| `contest_rating` | 70 | 30 | 50 | 30 | 35 | 30 | 60 |
| `project_count` | 75 | 60 | 80 | **90** | 75 | **80** | 70 |
| `communication_score` | 60 | **75** | 55 | 65 | 70 | **85** | 65 |
| `internship_exp` | 70 | 60 | 65 | 60 | 65 | **75** | 60 |

---

## 4. REST API Request & Response Parameters

### `POST /api/auth/register`
- **Request Body**:
  - `full_name` (`string`, required): Student name (1?150 chars).
  - `email` (`string`, required): Valid email address.
  - `password` (`string`, required): Password (min 6 chars).
  - `cohort_year` (`integer`, optional): Expected graduation year (e.g. 2026).
  - `academic_branch` (`string`, optional): Department name.
- **Success Response (201 Created)**:
  - `token` (`string`): Bearer JWT authentication token.
  - `user` (`object`): `{ student_id, full_name, email, cohort_year, academic_branch }`.

### `POST /api/auth/login`
- **Request Body**:
  - `email` (`string`, required): Registered email.
  - `password` (`string`, required): Account password.
- **Success Response (200 OK)**:
  - `token` (`string`): Bearer JWT authentication token.
  - `user` (`object`): User profile object.

### `POST /api/auth/guest`
- **Request Body**: None (Empty).
- **Success Response (200 OK)**:
  - `token` (`string`): Guest JWT token tied to demo account (`rohan@dron.ai`).
  - `user` (`object`): Demo user object.
  - `is_guest` (`boolean`): `true`.

### `GET /api/users/profile`
- **Headers**: `Authorization: Bearer <token>`
- **Success Response (200 OK)**:
  - `user`: Identity details (`student_id`, `full_name`, `email`, etc.).
  - `academic_records`: Array of semester objects (`semester`, `cgpa`, `attendance_pct`, `active_backlogs`).
  - `platform_links`: External handles (`github_username`, `leetcode_username`, `linkedin_url`, `last_synced`).
  - `skill_vector`: Quantitative metrics (`dsa_score`, `python_prof`, `total_commits`, etc.).

### `PUT /api/users/profile`
- **Request Body**:
  - `full_name` (`string`, optional)
  - `cohort_year` (`integer`, optional)
  - `academic_branch` (`string`, optional)
  - `academics` (`array`, optional): Updated semester records.
  - `skills` (`object`, optional): Updated self-assessed skill scores (0?100).
  - `platform_links` (`object`, optional): Updated GitHub/LeetCode usernames.
- **Success Response (200 OK)**: Updated complete profile object.

### `POST /api/metrics/fetch`
- **Request Body**:
  - `github_username` (`string`, optional)
  - `leetcode_username` (`string`, optional)
- **Success Response (200 OK)**:
  - `metrics`: `{ total_commits, problems_solved, contest_rating, last_synced }`.
  - `synced`: `true`.

### `POST /api/predictions/placement`
- **Request Body**: None (Evaluates active profile).
- **Success Response (200 OK)**:
  - `placement_probability` (`float`): Probability score between 0.0 and 1.0.
  - `readiness_tier` (`string`): Tier name ("Highly Prepared", etc.).
  - `is_placed` (`boolean`): Classification ($P \ge 0.50$).
  - `feature_importance` (`object`): Dictionary of feature keys to SHAP importance weights.
  - `top_factors` (`array[string]`): Top 3 driving features.

### `POST /api/career/recommend`
- **Request Body**: None (Evaluates active student vector).
- **Success Response (200 OK)**:
  - `recommendations` (`array`): Ranked list of careers:
    - `career` (`string`): Name of role (e.g., "Software Engineer").
    - `match_score` (`float`): Percentage match score (0.0 to 100.0).
    - `similarity` (`float`): Raw cosine similarity (0.0 to 1.0).
    - `description` (`string`): Description of role.

### `POST /api/roadmap/generate`
- **Request Body**:
  - `career` (`string`, optional): Selected role name (defaults to "Software Engineer").
- **Success Response (200 OK)**:
  - `target_career` (`string`): Target role.
  - `gaps` (`array`): Sorted list of deficits: `{ dimension, ideal, student, gap }`.
  - `roadmap` (`array`): Phased preparation plan:
    - `phase` (`integer`): Phase number (1, 2, 3).
    - `title` (`string`): Focus area (e.g. "Master Data Structures & Algorithms").
    - `duration` (`string`): Estimated timeline (e.g. "6 weeks").
    - `tasks` (`array[string]`): Concrete actionable learning tasks.

---

## 5. Environment & Configuration Parameters

| Parameter Name | Default in `config.py` | Description |
|:---|:---|:---|
| `SECRET_KEY` | `"dev-fallback-secret-key"` | Flask session signing key. Must be overridden in production. |
| `DATABASE_URL` | `"sqlite:///app/instance/dron_ai.db"` | SQLAlchemy connection URI (supports SQLite or MySQL). |
| `JWT_SECRET_KEY` | `"jwt-fallback-secret"` | Symmetric key used to sign and verify HMAC-SHA256 JWT tokens. |
| `JWT_ACCESS_TOKEN_EXPIRES`| `3600` (1 hour) | Token validity lifetime in seconds. |
| `GITHUB_PAT` | `""` (Empty string) | Optional GitHub Personal Access Token to increase rate limit from 60 to 5000 req/hr. |
| `ML_MODEL_DIR` | `ml_engine/saved_models` | Absolute directory path where `.pkl` and `.sha256` files reside. |
| `FLASK_ENV` | `"development"` | Active runtime environment (`development`, `testing`, `production`). |

---

# PART 2: COMPLETE UI FEATURES CATALOG

## 1. Global Design System & Common UI Components

The Dron AI frontend employs a modern, dark-mode, glassmorphism design system inspired by leading developer platforms:
- **Palette**: Deep Navy Canvas (`#0b0f19`), Card Surfaces (`#111827`), Subtle Borders (`#1f2937`), Accent Orange (`#ff7a00`), Neon Cyan (`#00f0ff`), Purple Focus (`#8b5cf6`), Emerald Success (`#10b981`), Amber Warning (`#f59e0b`), Rose Danger (`#f43f5e`).
- **Typography**: Clean sans-serif headings and body text (`Outfit`, `Inter`) paired with `JetBrains Mono` for code snippets and metric percentages.
- **Glassmorphic Cards**: Semi-transparent backdrops (`backdrop-filter: blur(12px)`) with subtle gradient borders.
- **Navigation Architecture**: Fixed collapsible left sidebar (`app-sidebar`) with mobile hamburger drawer and floating top bar (`app-header`).
- **Toast Notifications**: Dynamically spawned non-blocking alert toasts (success, warning, error) that auto-dismiss after 4 seconds.

---

## 2. Screen-by-Screen UI Feature Breakdown

### Screen 1: `index.html` (Unified Master Intelligence Dashboard)
*The central single-page executive control center containing the full 5-stage progression pipeline:*

1. **Top Header & Student Welcome Bar**:
   - Dynamic personalized greeting: *"Welcome back, [Student Name]"*.
   - Live readiness status pill: Shows current tier (e.g. `Highly Prepared`) with color-coded dot.
   - Quick Navigation Links to dedicated detailed pages (`Profile`, `Predictions`, `Career`, `Roadmap`).
   - Logout button with instant JWT cache invalidation.

2. **Stage 1: Profile & Academic Data Entry Widget**:
   - **Identity Inputs**: Full Name input, Cohort Year selector, Academic Branch dropdown.
   - **Academic Progression Inputs**: Current Semester selector (1 to 8), Cumulative CGPA input (0.00 to 10.00), Attendance Percentage input (0 to 100), Active Backlogs counter.
   - **Save Profile Button**: Saves data asynchronously to `/api/users/profile` with spinner state.

3. **Stage 2: Synced Developer Metrics Widget**:
   - **Platform Handle Inputs**: GitHub username input, LeetCode username input, LinkedIn URL.
   - **Live Sync Button**: Triggers `/api/metrics/fetch` with real-time fetching pulse animation.
   - **Metrics Summary Cards**:
     - *GitHub Commits Card*: Displays total commits with branch activity icon.
     - *LeetCode Problems Card*: Displays total solved count.
     - *Contest Rating Card*: Displays official rating pill.
     - *Projects Count Card*: Displays completed resume projects.
     - *Last Synced Badge*: Displays relative time (e.g. *"Synced 5m ago"*).

4. **Stage 3: Placement Readiness (XGBoost) Analytics Widget**:
   - **Trigger Button**: *"Run Placement Prediction"* button with glowing gradient pulse.
   - **Circular Radial Gauge / Score Meter**: Visual dial animating from 0% to student's computed placement probability.
   - **Readiness Tier Badge**: Large bold pill (`Highly Prepared`, `Prepared`, `Needs Improvement`, `High Risk`).
   - **Key Contributing Factors List**: Top 3 influential features extracted via SHAP attribution (e.g. `+ dsa_score (0.34)`, `+ cgpa (0.28)`).

5. **Stage 4: Career Recommendations Widget**:
   - **Trigger Button**: *"Match Target Careers"* button.
   - **Horizontal Card Deck of Career Matches**: Displays ranked tech roles (Software Engineer, ML Engineer, Data Analyst, etc.).
   - **Match Percentage Bars**: Color-coded progress bar indicating cosine similarity percentage (e.g. `91.4% Match`).
   - **Role Selection Button**: Clicking *"Select as Target"* locks the role as active and instantly updates the Stage 5 roadmap.

6. **Stage 5: Skill Gap Analysis & Personalized Roadmap Widget**:
   - **Active Target Role Header**: Displays currently selected career benchmark.
   - **Vector Deficit Breakdown**: Horizontal comparison bars showing student's skill score vs. the ideal career benchmark (e.g. *DSA Score: 62 / 90 ? -28 deficit*).
   - **Phased Action Plan Accordion / Timeline**:
     - Phase 1: Foundation & Urgent Gaps (e.g. LeetCode Easy & Arrays).
     - Phase 2: Core Pattern Mastery (e.g. Graphs, DP, Trees).
     - Phase 3: Project Capstone & Mock Interview Simulation.
   - **Interactive Task Checkboxes**: Students can check off completed tasks; dynamically recalculates roadmap completion percentage.

---

### Screen 2: `login.html` (Student Authentication Screen)
- **Branded Header**: Dron AI logo icon with subtitle *"Career Intelligence & Placement Platform"*.
- **Email Input Field**: With mail icon, placeholder `student@university.edu`, and regex email validation.
- **Password Input Field**: With lock icon and *"Show/Hide Password"* eye toggle button.
- **Remember Me Checkbox**: Persists authentication token across browser sessions.
- **Primary Submit Button**: *"Sign In to Dashboard"* with loading spinner state on click.
- **Quick 1-Click Guest Mode Button**: *"Explore as Demo Student (Rohan Jha)"* ? bypasses registration for instant evaluators.
- **Switch to Register Link**: Direct link to `register.html`.

---

### Screen 3: `register.html` (Student Onboarding Screen)
- **Full Name Input**: Validates name presence.
- **University Email Input**: Checks uniqueness via backend API.
- **Password & Confirm Password Inputs**: Client-side match verification and minimum 6-character length enforcement.
- **Cohort Year Dropdown**: Selectable graduation years (2024, 2025, 2026, 2027, 2028).
- **Academic Branch Dropdown**: Options for `Computer Science & Engineering`, `Information Technology`, `Electronics & Communication`, `Electrical Engineering`, `Mechanical Engineering`.
- **Create Account Button**: Triggers `/api/auth/register` and auto-redirects to `index.html` upon token receipt.
- **Switch to Login Link**: Direct link to `login.html`.

---

### Screen 4: `profile.html` (Dedicated Profile & Academic History Page)
- **Student Profile Overview Card**: Displays student avatar initials, registered email, department, and cohort year.
- **Semester Progression Data Table**:
  - Displays historical records for Semesters 1 through 8.
  - Columns: *Semester*, *CGPA*, *Attendance %*, *Backlogs*, *Actions (Edit/Delete)*.
  - Add Semester Modal / Row Input.
- **Platform Connection Hub**:
  - GitHub connection status card with verified username badge.
  - LeetCode connection status card with contest rating badge.
  - LinkedIn profile link input.
  - Manual sync trigger button.
- **Technical Skills Self-Assessment Form**:
  - Range Sliders (0 to 100) for *DSA*, *Python*, *C++*, *AI/ML*, and *Soft Skills*.
  - Real-time numerical value indicators updating on slider drag.
  - *"Save All Profile Changes"* floating action button.

---

### Screen 5: `career.html` (Dedicated Career Matching Hub)
- **Hero Methodology Banner**: Explains mathematical cosine vector comparison against industry roles.
- **Target Role Filter Buttons**: Filter by all roles, software engineering, data & AI, or systems & security.
- **Comprehensive Career Match Cards** (7 roles):
  - Card Title (e.g. *Machine Learning Engineer*).
  - Career Description & typical industry responsibilities.
  - Cosine Match Percentage Circular Pill.
  - Core Competency Breakdown Grid: Highlights required skills vs. student's current proficiency.
  - *"Set as Active Target Role"* CTA button with visual checkmark indicator.

---

### Screen 6: `predictions.html` (Dedicated Placement Analytics Page)
- **High-Impact Placement Readiness Gauge**:
  - Central 240px radial gauge with animated stroke and glowing gradient.
  - Large percentage readout (e.g. `84.2%`).
  - Readiness Tier announcement banner (`Highly Prepared`).
- **Explainable AI (SHAP) Factor Breakdown**:
  - Horizontal bar chart showing positive vs. negative attribution factors.
  - Feature name label, contribution weight, and plain-English explanation (e.g. *"Strong LeetCode rating (+1800) boosted your probability by +14.2%"*).
- **Faculty Mentor & AI Recommendation Commentary**:
  - Tailored advice paragraph dynamically assembled from the student's top weaknesses.
  - Direct CTA button: *"Proceed to Remediation Roadmap"*.

---

### Screen 7: `roadmap.html` (Skill-Gap Remediation & Phased Roadmap Page)
- **Vector Gap Analyzer Bar Chart**:
  - Comparative dual bars for each of the 10 skill dimensions:
    - Bar 1: Student's current score.
    - Bar 2: Ideal target role requirement.
    - Delta Badge: Showing net deficit (e.g. `-25 pts`).
- **Prioritized Deficiency Cards**:
  - Categorizes gaps into *Critical Gaps* (deficit $> 30$), *Moderate Gaps* (deficit $15?30$), and *Minor Gaps* (deficit $< 15$).
- **Phased Milestone Learning Plan**:
  - **Phase 1 (Weeks 1?4)**: Foundational DSA & Core Patterns.
  - **Phase 2 (Weeks 5?8)**: System Design, Advanced Algorithms, and Mock Contests.
  - **Phase 3 (Weeks 9?12)**: Capstone Project Deployment & Behavioral Interview Prep.
- **Interactive Checkable Milestones**:
  - Checkboxes that persist state across page reloads.
  - Real-time progress bar: *"4 of 12 Tasks Completed (33%)"*.
