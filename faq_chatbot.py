import string
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download necessary NLTK assets
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

# 1. Collect FAQs (Knowledge Base)
faq_data = [
    {
        "question": "What is your return policy?",
        "answer": "You can return any product within 30 days of purchase for a full refund."
    },
    {
        "question": "How long does shipping take?",
        "answer": "Standard shipping takes 3-5 business days. Express shipping takes 1-2 days."
    },
    {
        "question": "Can I track my order?",
        "answer": "Yes, once your order ships, we will email you a tracking link to follow its progress."
    },
    {
        "question": "What payment methods do you accept?",
        "answer": "We accept all major credit cards, PayPal, and Apple Pay."
    },
    {
        "question": "How can I contact customer support?",
        "answer": "You can reach our support team via email at support@example.com or call 1-800-555-0199."
    }
]

# Extract questions and answers for processing
faq_questions = [faq["question"] for faq in faq_data]
faq_answers = [faq["answer"] for faq in faq_data]

# 2. Text Preprocessing Function
def preprocess_text(text):
    # Lowercase the text
    text = text.lower()
    # Tokenize words
    tokens = word_tokenize(text)
    # Remove punctuation and stop words
    stop_words = set(stopwords.words('english'))
    cleaned_tokens = [
        word for word in tokens 
        if word not in string.punctuation and word not in stop_words
    ]
    # Rejoin tokens back into a clean string
    return " ".join(cleaned_tokens)

# Preprocess all target FAQ questions
preprocessed_faqs = [preprocess_text(q) for q in faq_questions]

# 3. Match User Question & Return Answer
def get_chatbot_response(user_query, similarity_threshold=0.2):
    # Clean the incoming user query
    cleaned_query = preprocess_text(user_query)
    
    # Initialize TF-IDF Vectorizer with our preprocessing logic
    vectorizer = TfidfVectorizer()
    
    # Fit and transform the FAQ corpus along with the user query
    corpus = preprocessed_faqs + [cleaned_query]
    tfidf_matrix = vectorizer.fit_transform(corpus)
    
    # Calculate cosine similarity between the user query (last row) and all FAQs
    vectors = tfidf_matrix[:-1]
    query_vector = tfidf_matrix[-1]
    similarities = cosine_similarity(query_vector, vectors).flatten()
    
    # Find the index of the highest similarity score
    best_match_idx = similarities.argmax()
    highest_score = similarities[best_match_idx]
    
    # Check if the match is confident enough
    if highest_score >= similarity_threshold:
        return faq_answers[best_match_idx]
    else:
        return "I'm sorry, I couldn't find an answer to that question. Would you like to contact support?"

# 4. User Interaction Interface (Terminal Chat Loop)
if __name__ == "__main__":
    print("🤖 FAQ Chatbot initialized! Type 'exit' or 'quit' to close the session.\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            print("🤖 Chatbot: Goodbye!")
            break
        
        response = get_chatbot_response(user_input)
        print(f"🤖 Chatbot: {response}\n")