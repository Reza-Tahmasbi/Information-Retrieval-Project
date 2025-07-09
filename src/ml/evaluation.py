import datetime
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
from sklearn.metrics.cluster import contingency_matrix
from sklearn.metrics import adjusted_rand_score, classification_report, confusion_matrix, f1_score, precision_score, recall_score
import os

def evaluate_classifier(y_true, y_pred, classifier_name, project='wiki'):
    print(f"\nEvaluation for {classifier_name} ({project} project):")
    print("\nClassification Report:")
    report = classification_report(y_true, y_pred)
    print(report)
    
    # Calculate metrics
    f1 = f1_score(y_true, y_pred, average='weighted')
    precision = precision_score(y_true, y_pred, average='weighted')
    recall = recall_score(y_true, y_pred, average='weighted')
    
    print(f"F1 Score: {f1:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    
    # Confusion Matrix
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(8,6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title(f'Confusion Matrix - {classifier_name} ({project})')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    
    # Define output directory
    output_dir = os.path.join(os.path.dirname(__file__), '../../output', project)
    os.makedirs(output_dir, exist_ok=True)
    
    # Save confusion matrix as image
    cm_path = os.path.join(output_dir, f'confusion_matrix_{classifier_name.lower().replace(" ", "_")}.png')
    plt.savefig(cm_path)
    plt.close()
    
    # Save classification report to text file
    report_path = os.path.join(output_dir, f'classification_report_{classifier_name.lower().replace(" ", "_")}.txt')
    with open(report_path, 'w') as f:
        f.write(f"Evaluation for {classifier_name} ({project} project):\n\n")
        f.write("Classification Report:\n")
        f.write(report)
        f.write(f"\nF1 Score: {f1:.4f}\n")
        f.write(f"Precision: {precision:.4f}\n")
        f.write(f"Recall: {recall:.4f}\n")
    
    return f1, precision, recall

def evaluate_clustering(y_true, clusters, project='wiki'):
    # Purity
    cont_matrix = contingency_matrix(y_true, clusters)
    purity = np.sum(np.amax(cont_matrix, axis=0)) / np.sum(cont_matrix)
    
    # Rand Index
    rand_index = adjusted_rand_score(y_true, clusters)
    
    print(f"\nClustering Evaluation ({project} project):")
    print(f"Purity: {purity:.4f}")
    print(f"Rand Index: {rand_index:.4f}")

    output_dir = os.path.join(os.path.dirname(__file__), f'../../output', project)
    os.makedirs(output_dir, exist_ok=True)
    
    # Save clustering metrics to text file
    metrics_path = os.path.join(output_dir, 'clustering_metrics.txt')
    with open(metrics_path, 'a') as f:  # 'a' for append to avoid overwriting
        f.write(f"\nClustering Evaluation ({project} project) at {datetime.datetime.now()}:\n")
        f.write(f"Purity: {purity:.4f}\n")
        f.write(f"Rand Index: {rand_index:.4f}\n")
    
    return purity, rand_index