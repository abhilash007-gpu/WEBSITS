# Internship Lab — Data Science & Applied AI

Three practical portfolio demos by Abhilash Panchal:

1. **RetailPulse** — retail analytics dashboard with Python/Pandas calculations and SQL business questions.
2. **ChurnLens** — scikit-learn Logistic Regression churn classifier with a probability simulator and held-out evaluation.
3. **DocuMind** — document retrieval prototype with chunk ranking and visible source references.

## Try the demo
Open the deployed site and use the top navigation to switch between all three projects.

## Data and model transparency
RetailPulse uses deterministic synthetic sample orders generated in the browser for its interactive dashboard. The Python data pipeline generates a reproducible CSV for analysis.
ChurnLens metrics were calculated using a stratified 75/25 split on a deterministic synthetic customer dataset. The model was trained with a scikit-learn pipeline and its coefficients were exported for the browser demo. The metrics are not evidence of real-world performance.
DocuMind demonstrates lexical retrieval over a small sample knowledge base. It does not claim to call an LLM in this static version.

## Run locally
```bash
python -m http.server 8000
```
Visit http://localhost:8000. Python workflow requirements are in `requirements.txt`.

## Reproduce the data and model
```bash
python -m pip install -r requirements.txt
python scripts/generate_data.py
python scripts/analyze_sales.py
python scripts/train_churn.py
python scripts/rag_engine.py "Which metrics should I explain for a churn model?"
python -m unittest discover -s tests -v
```

## Interview walkthrough
For each project, explain:
- the business or user problem and the dataset limitations;
- one calculation, SQL query or model decision;
- how you checked the output;
- what you personally changed or improved;
- one next step you would implement.

**Do not list technologies you cannot explain.** Use the learning guide to study, then make a small contribution of your own before adding the project to your resume.
