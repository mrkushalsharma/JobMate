import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Download required NLTK data
nltk.download('punkt')
nltk.download('stopwords')

def calculate_match_score(resume_text: str, job_description: str):
    # Preprocess texts
    stop_words = set(stopwords.words('english'))

    def preprocess(text):
        tokens = word_tokenize(text.lower())
        filtered_tokens = [word for word in tokens if word.isalnum() and word not in stop_words]
        return " ".join(filtered_tokens)

    processed_resume = preprocess(resume_text)
    processed_job = preprocess(job_description)

    # Create TF-IDF vectors
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([processed_resume, processed_job])

    # Calculate cosine similarity
    similarity = cosine_similarity(vectors[0:1], vectors[1:2])

    # Return score as percentage
    return float(similarity[0][0] * 100)

