# SmartDeduct: UC717 Dynamic Deductible Optimizer

SmartDeduct is a responsive, localhost-based insurance decision-support prototype. It compares deductible options using a customer's financial profile, claim expectations, risk preference, and insurance type, then recommends the most suitable option through transparent rule-based scoring.

> **Important:** All included customer data, deductible values, discounts, scores, and recommendations are synthetic and intended only for prototype demonstration. This application is not an insurance quotation, underwriting decision, policy recommendation, or financial advice.

## Problem Statement

Insurance customers may not clearly understand the trade-off between:

- Annual insurance premium
- Deductible amount
- Claim-time out-of-pocket cost
- Emergency savings and affordability
- Claim frequency and risk preference

A high deductible may reduce the premium but create financial difficulty during a claim. A low deductible may be safer during a claim but result in a higher annual premium.

## Solution

The application:

1. Loads a preconfigured customer and deductible dataset or accepts CSV/XLSX uploads.
2. Validates required columns, values, customer IDs, risk preferences, and insurance types.
3. Displays all successfully loaded customers in an ID-and-name dropdown.
4. Connects the customer and deductible datasets using `insurance_type`.
5. Calculates affordability, expected claim cost, expected annual cost, premium savings, and suitability.
6. Ranks the matching deductible options.
7. Displays a recommendation, comparison table, chart, and downloadable analysis.

## Key Features

- Responsive Bootstrap user interface
- Dedicated and clearly visible Data Upload Center
- Preloaded dataset for immediate demonstration
- External CSV and XLSX customer uploads
- Optional external deductible upload
- Preloaded deductible fallback when no deductible file is supplied
- Downloadable customer and deductible templates
- Detailed file-validation messages
- Customer filtering by insurance type
- Customer ID and name selection
- Insurance-specific deductible matching
- Metric cards, option-comparison table, and Chart.js visualization
- Downloadable analysis CSV
- No external API required

## Relationship Between Datasets

The customer and deductible tables are connected by `insurance_type`.

```text
Motor customer   -> Motor or All deductible options
Property customer -> Property or All deductible options
Health customer  -> Health or All deductible options
```

The deductible dataset does not require `customer_id`. The same insurance-specific options can be evaluated for multiple customers.

## Technology Stack

- Python
- Flask
- Pandas
- OpenPyXL
- HTML5
- CSS3
- JavaScript
- Bootstrap 5
- Chart.js
- CSV and XLSX files

## Project Structure

```text
UC717_Bootstrap_Updated/
├── app.py
├── requirements.txt
├── README.md
├── data/
│   ├── customers.csv
│   └── deductible_options.csv
├── download_templates/
│   ├── customer_upload_template.csv
│   └── deductible_upload_template.csv
├── sample_uploads/
│   ├── upload_customers_25.csv
│   └── upload_deductibles.csv
├── static/
│   ├── css/style.css
│   └── js/app.js
└── templates/
    └── index.html
```

## Run Locally in VS Code

### 1. Open the project folder

Open `UC717_Bootstrap_Updated` in VS Code and start a new terminal.

### 2. Create a virtual environment

```powershell
python -m venv venv
```

### 3. Activate the virtual environment

```powershell
venv\Scripts\Activate.ps1
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 5. Start the application

```powershell
python app.py
```

### 6. Open the application

```text
http://127.0.0.1:5000
```

## Upload and Analyze Data

### Using preloaded data

1. Click **Preloaded Data**.
2. Select an insurance filter.
3. Select a customer ID and name.
4. Click **Analyze Options**.

### Uploading external data

1. Click **Upload Data**.
2. Upload `sample_uploads/upload_customers_25.csv` as the customer dataset.
3. Optionally upload `sample_uploads/upload_deductibles.csv`.
4. Click **Validate and Load Datasets**.
5. Confirm the success message.
6. Select a customer.
7. Click **Analyze Options**.

If the deductible file is not uploaded, the application uses the preloaded deductible dataset.

## Upload File Requirements

### Customer dataset

```text
customer_id
customer_name
monthly_income
monthly_expenses
emergency_savings
current_annual_premium
expected_claims_per_year
average_claim_amount
risk_preference
insurance_type
```

Accepted `risk_preference` values: `Low`, `Medium`, `High`.

Accepted `insurance_type` values: `Motor`, `Property`, `Health`.

### Deductible dataset

Required columns:

```text
insurance_type
deductible
premium_discount_pct
```

Accepted `insurance_type` values: `Motor`, `Property`, `Health`, `All`.

Use `10` for a 10% discount, not `0.10` or `10%`.

## Calculation Overview

```text
Disposable income = Monthly income - Monthly expenses
Estimated premium = Current premium x (1 - Discount / 100)
Premium saving = Current premium - Estimated premium
Expected claim cost = Expected claims x Minimum(Deductible, Average claim amount)
Expected annual cost = Estimated premium + Expected claim cost
```

The final suitability score combines affordability, expected cost, risk preference, deductible exposure, and expected claim frequency.

## Current-State Architecture

```text
Browser UI
   -> Flask validation endpoints
   -> Pandas calculation engine
   -> Local CSV/XLSX datasets
   -> Recommendation and downloadable result
```

## Future Enhancements

- Insurer policy and claims APIs
- Authentication and role-based access
- Secure database and cloud deployment
- Historical-data machine-learning risk model
- Optional LLM-generated explanation layer
- LangChain or LangGraph workflow orchestration
- Human approval, audit logs, monitoring, and fairness review

## GitHub Upload Through VS Code

Create a `.gitignore` file before committing:

```gitignore
venv/
__pycache__/
*.pyc
.env
.vscode/
.DS_Store
```

Then run:

```powershell
git init
git add .
git commit -m "Add UC717 Dynamic Deductible Optimizer prototype"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
git push -u origin main
```

## Demo Presentation

The repository can include `UC717_Project_Presentation.pptx`, a four-slide summary covering:

1. Project overview
2. Problem, objective, and business value
3. Prototype workflow and key features
4. Architecture, technology, and future roadmap

## License

This project is intended for internal learning and proof-of-concept demonstration. Add your organization's approved license before public or production distribution.
