# UC717 Bootstrap Updated

## Run in VS Code
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5000

## Upload test
Use files in `sample_uploads`. Customer upload is required; deductible upload is optional. Click Validate and load datasets, select a customer, then Analyze options.

Customer and deductible tables relate through `insurance_type`.
