import os
import re
import nltk
import numpy as np
import pandas as pd
import arabic_reshaper
from hazm import Lemmatizer
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from nltk.corpus import stopwords
from bidi.algorithm import get_display
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer


def load_data(file_path, project='wiki'):
    df = pd.read_csv(file_path)
    # Select appropriate text column based on project
    if project == 'digi':
        df['Text'] = df['Title'].fillna('')  # Use Title for Digikala, handle NaN
    else:  # Assume 'wiki' or default
        df['Text'] = df.get('Main_Text', df.get('Title', '')).fillna('')  # Fallback to Title if Main_Text missing
    return df

def preprocess_text(text, project='wiki'):
    if not isinstance(text, str):
        return ''
    
    # Lowercase (optional for Persian, but consistent with English)
    text = text.lower()
    
    # Define character handling based on project
    if project == 'digi':
        # Keep Persian characters and basic Latin, remove other special characters
        text = re.sub(r'[^\u0600-\u06FF\u0750-\u077Fa-zA-Z\s]', '', text)  # Persian range + Latin
    else:  # 'wiki' or default
        # Remove non-Latin characters (English-focused)
        text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # Tokenize
    tokens = word_tokenize(text)
    
    # Remove stopwords based on project
    if project == 'digi':
        # Persian stopwords (if available) or fallback to English
        try:
            import hazm
            stop_words = set(hazm.stopwords_list())  # Requires 'hazm' package for Persian
        except ImportError:
            stop_words = set(stopwords.words('english'))  # Fallback to English
    else:  # 'wiki' or default
        stop_words = set(stopwords.words('english'))
    
    tokens = [token for token in tokens if token not in stop_words]
    
    # Lemmatize
    lemmatizer = Lemmatizer() if project == 'digi' else WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    
    return ' '.join(tokens)

# 3. Feature extraction
def extract_features(texts, project='wiki'):
    # Adjust max_features or ngram_range based on project if needed
    tfidf = TfidfVectorizer(max_features=5000, ngram_range=(1,2))
    features = tfidf.fit_transform(texts)
    return features, tfidf

# Word Cloud visualization
def generate_wordcloud(texts, title, project='wiki'):
    font_path = '../../asset/tahoma.ttf'
    text = ' '.join(texts)
    reshaped_text = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_text)
    wordcloud = WordCloud(font_path=font_path, width=800, height=400, background_color='white').generate(text)
    plt.figure(figsize=(10,5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(title)
    
    # Define output directory
    output_dir = os.path.join(os.path.dirname(__file__), '../../output', project)
    os.makedirs(output_dir, exist_ok=True)
    
    # Save word cloud image
    image_path = os.path.join(output_dir, f'wordcloud_{title.lower().replace(" ", "_")}.png')
    plt.savefig(image_path)
    plt.close()