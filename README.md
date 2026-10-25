# Matchly — Resume Matcher

Matchly is a machine learning mini-project that compares a resume with a job description and calculates a text-similarity score.

## Features

- Upload a resume in PDF format.
- Extract resume text using PyMuPDF.
- Paste a job description.
- Calculate text similarity using TF-IDF and cosine similarity.
- View the results through a Streamlit web interface.

## Technologies Used

- Python
- Streamlit
- Scikit-learn
- PyMuPDF
- TF-IDF
- Cosine Similarity

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

## Project Structure

- `app.py` — Streamlit user interface.
- `matcher.py` — Machine learning similarity logic.
- `requirements.txt` — Required Python libraries.

## Limitations

The similarity score measures textual similarity, not the probability of getting hired. The current version does not perform missing-skills analysis.

## Author

Anushka Singh