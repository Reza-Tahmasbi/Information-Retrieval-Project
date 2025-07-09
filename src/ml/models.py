# Classification with 3 algorithms
from sklearn.calibration import LinearSVC
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB


def train_classifiers(X_train, y_train):
    # Naive Bayes
    nb = MultinomialNB()
    nb.fit(X_train, y_train)
    
    # Linear SVM
    svm = LinearSVC()
    svm.fit(X_train, y_train)
    
    # Random Forest
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)
    
    return nb, svm, rf

    # Clustering
def perform_clustering(X, n_clusters=4):
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    clusters = kmeans.fit_predict(X)
    return clusters