from sklearn.model_selection import train_test_split
from evaluation import evaluate_classifier, evaluate_clustering
from models import perform_clustering, train_classifiers
from modules import extract_features, generate_wordcloud, load_data, preprocess_text
import os

def select_path(project):
    """Select the CSV file path based on the project."""
    path_dict = {
        'wiki': '../../data/csv/wiki_data.csv',
        'digi': '../../data/csv/digi_data.csv'
    }
    return path_dict.get(project, '../../data/csv/wiki_data.csv')  # Default to wiki if project not found

def main(project, file_path):
    # Load data
    df = load_data(file_path, project=project)
    
    # Preprocess text
    df['Processed_Text'] = df['Text'].apply(lambda x: preprocess_text(x, project=project))
    
    # Generate word clouds for each category
    for category in df['Category'].unique():
        category_texts = df[df['Category'] == category]['Processed_Text']
        generate_wordcloud(category_texts, f'Word Cloud for {category}', project)
    
    # Feature extraction
    X, tfidf = extract_features(df['Processed_Text'])
    y = df['Category']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42)
    
    # Train and evaluate classifiers
    nb, svm, rf = train_classifiers(X_train, y_train)
    
    # Evaluate Naive Bayes
    nb_pred = nb.predict(X_test)
    nb_metrics = evaluate_classifier(y_test, nb_pred, "Naive Bayes", project=project)
    
    # Evaluate SVM
    svm_pred = svm.predict(X_test)
    svm_metrics = evaluate_classifier(y_test, svm_pred, "Linear SVM", project=project)
    
    # Evaluate Random Forest
    rf_pred = rf.predict(X_test)
    rf_metrics = evaluate_classifier(y_test, rf_pred, "Random Forest", project=project)
    
    # Perform and evaluate clustering
    clusters = perform_clustering(X)
    cluster_metrics = evaluate_clustering(y, clusters, project=project)
    
    # Store results
    results = {
        'Naive Bayes': nb_metrics,
        'Linear SVM': svm_metrics,
        'Random Forest': rf_metrics,
        'Clustering': cluster_metrics
    }
    
    return results

if __name__ == "__main__":
    project = 'digi'  # or 'digi'
    file_path = os.path.join(os.path.dirname(__file__), select_path(project))
    results = main(project, file_path)
    print("Results:", results)