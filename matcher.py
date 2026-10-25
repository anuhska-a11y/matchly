
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_similarity(resume_text, job_description):
    # Combine both texts into numerical features
    documents = [resume_text, job_description]

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)

    # Calculate similarity between the two texts
    similarity = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:2]
    )[0][0]

    # Convert the score into a percentage
    return round(similarity * 100, 2)


if __name__ == "__main__":
    resume = """
    Python, Machine Learning, Pandas, SQL,
    Data Analysis, Scikit-learn
    """

    job_description = """
    Python developer with Machine Learning,
    SQL, NLP and data analysis skills
    """

    score = calculate_similarity(resume, job_description)

    print(f"Resume-Job Similarity: {score}%")
