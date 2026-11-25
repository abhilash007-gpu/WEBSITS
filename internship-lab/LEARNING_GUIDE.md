# Learning Guide — Understand the Projects

Start with the problem and trace the code. Do not memorise explanations you cannot reproduce.

## 1. RetailPulse — Analytics, SQL and Python
A shop has many orders and wants to know which categories and regions generate revenue and gross profit.

- **CSV:** a text-based table. Each row is one order.
- **Pandas:** a Python library for working with tables. `read_csv()` loads data and `groupby()` aggregates rows.
- **SQL:** use `SELECT` to choose columns, `WHERE` to filter rows, `GROUP BY` to aggregate categories and `ORDER BY` to sort.
- **Revenue:** units × selling price × (1 − discount).
- **Gross profit:** revenue − units × unit cost.
- **Profit margin:** profit ÷ revenue × 100.

Study tasks: run the Python analysis, read each SQL query, add an average-order-value KPI and explain why revenue alone is not enough.

Interview questions:
1. Difference between WHERE and HAVING?
2. Why should duplicate order IDs be checked?
3. What happens when revenue is zero while calculating margin?
4. How would you investigate a region with high revenue but low profit?

## 2. ChurnLens — Machine Learning
The goal is to estimate whether a subscription customer may leave based on historical examples.

- **Feature:** an input such as tenure or number of support tickets.
- **Target:** the answer being predicted. Here, churned is 1 or 0.
- **Train/test split:** train using one subset and evaluate on records not used for fitting.
- **Imputation:** fill missing values using a rule such as the median.
- **Scaling:** put numeric features on comparable scales.
- **One-hot encoding:** convert text categories into numeric indicator columns.
- **Logistic regression:** calculates a weighted score and converts it into a probability.
- **Pipeline:** keeps preprocessing and model training together to avoid data leakage.

Metrics:
- Accuracy = fraction of all predictions that are correct.
- Precision = among predicted churners, how many actually churned?
- Recall = among actual churners, how many did the model catch?
- F1 = balance of precision and recall.
- ROC-AUC = how well model scores rank positive cases above negative ones.
- Confusion matrix = true negatives, false positives, false negatives and true positives.

Study tasks: explain stratification, why scaling is fit only on training data, and how changing a threshold affects precision/recall. Run `scripts/train_churn.py` and compare its output.

## 3. DocuMind — Retrieval and RAG
The app searches documents and retrieves relevant passages so a user can verify the evidence.

- **Chunking:** split long documents into smaller overlapping pieces.
- **Tokenization:** turn text into searchable terms.
- **Retrieval:** rank chunks by relevance to a question.
- **RAG:** retrieve evidence first, then provide it to a language model to generate a grounded answer.
- **Citation:** show which source passages support a response.

This static demo implements lexical retrieval and source references. It does not claim to provide a generated LLM answer.

Study tasks: explain why chunk overlap matters, how keyword retrieval differs from embeddings, and how you would evaluate the relevance of retrieved passages.

## 7-day study plan
| Day | Focus | Practice output |
|---|---|---|
| 1 | CSV, Pandas and KPI formulas | Explain sales revenue and profit |
| 2 | SQL SELECT, WHERE, GROUP BY | Write 5 queries without copying |
| 3 | Dashboard insights | Present 3 findings |
| 4 | Features and train/test split | Explain the churn dataset |
| 5 | Logistic regression and metrics | Explain the confusion matrix |
| 6 | Chunking and retrieval | Walk through a cited DocuMind answer |
| 7 | Git, deployment and interview practice | Give a 3-minute walkthrough of each |

## Make the projects yours
- [ ] Add a new KPI or filter to RetailPulse and commit it.
- [ ] Write one SQL query independently.
- [ ] Change the churn decision threshold and compare precision/recall.
- [ ] Add a new document to DocuMind and test five questions.
- [ ] Write your own project summary in your own words.

You are ready to discuss a project when you can explain the problem, data, pipeline, one result, one limitation and one improvement without reading from the screen.
