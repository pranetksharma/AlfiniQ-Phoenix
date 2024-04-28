import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt
import warnings
import joblib

# Suppress future warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

def load_and_clean_data(file_path):
    """
    Load and clean the dataset by removing specific columns and rows with NaN values.

    Args:
    file_path (str): The path to the dataset file.

    Returns:
    pd.DataFrame: A cleaned pandas DataFrame.
    """
    data = pd.read_excel(file_path, index_col=None)
    df_clean = data.dropna()
    df_clean = df_clean.drop(columns=['vacc_miss_MMR', 'vacc_miss_DTP', 'vacc_miss_HBV', 'vacc_miss_TB', 'vacc_miss_pol', 'educ_prov'])
    return df_clean

def preprocess_data(df):
    """
    Preprocess the data by converting object type columns to numeric and scaling the data.

    Args:
    df (pd.DataFrame): The DataFrame to preprocess.

    Returns:
    np.ndarray: Scaled data as a numpy array.
    """
    object_columns = df.select_dtypes(include='object').columns
    for column in object_columns:
        df[column] = pd.to_numeric(df[column], errors='coerce')

    imputer = SimpleImputer(strategy='median')
    data_imputed = imputer.fit_transform(df)

    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(data_imputed)
    return data_scaled

def apply_pca(data, n_components=2):
    """
    Apply PCA to reduce dimensions of data.

    Args:
    data (np.ndarray): Data to apply PCA.
    n_components (int): Number of principal components to keep.

    Returns:
    np.ndarray: Data transformed into principal components.
    """
    pca = PCA(n_components=n_components)
    data_pca = pca.fit_transform(data)
    return data_pca

def perform_kmeans(data, n_clusters):
    """
    Perform KMeans clustering on the data.

    Args:
    data (np.ndarray): Data on which to perform clustering.
    n_clusters (int): Number of clusters to form.

    Returns:
    np.ndarray: Cluster labels for each point in the dataset.
    """
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    clusters = kmeans.fit_predict(data)
    return clusters

def plot_clusters(data, clusters):
    """
    Plot the results of clustering.

    Args:
    data (np.ndarray): Data reduced to two principal components.
    clusters (np.ndarray): Cluster labels for each point.

    Returns:
    None: Displays a scatter plot of the clusters.
    """
    plt.figure(figsize=(8, 6))
    plt.scatter(data[:, 0], data[:, 1], c=clusters, marker='o')
    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')
    plt.title('PCA and KMeans Clustering Results')
    plt.colorbar(label='Cluster label')
    plt.show()

def create_synthetic_data(n_samples, n_features, centers, cluster_std, noise_level):
    """
    Generate synthetic data with blobs for clustering analysis.

    Args:
    n_samples (int): Number of samples to generate.
    n_features (int): Number of features for each sample.
    centers (int): Number of centers to generate.
    cluster_std (float): Standard deviation of the clusters.
    noise_level (float): Standard deviation of the Gaussian noise added to the data.

    Returns:
    tuple: A tuple containing the features and labels of the synthetic data.
    """
    X, y = make_blobs(n_samples=n_samples, n_features=n_features, centers=centers, cluster_std=cluster_std, random_state=42)
    noise = np.random.normal(0, noise_level, X.shape)
    X_noisy = X + noise
    return X_noisy, y

def train_random_forest(X_train, y_train):
    """
    Train a Random Forest classifier on the training data.

    Args:
    X_train (np.ndarray): Features of the training data.
    y_train (np.ndarray): Labels of the training data.

    Returns:
    RandomForestClassifier: Trained Random Forest classifier.
    """
    rf_model = RandomForestClassifier(random_state=42)
    rf_model.fit(X_train, y_train)
    return rf_model

def save_model(model, file_name):
    """
    Save the trained model to a file.

    Args:
    model (RandomForestClassifier): Trained model to save.
    file_name (str): Path to save the model.
    
    Returns:
    None: Saves the model to the specified file path.
    """
    joblib.dump(model, file_name)

def load_model(file_name):
    """
    Load a model from a file.

    Args:
    file_name (str): Path to the model file.

    Returns:
    RandomForestClassifier: Loaded model.
    """
    return joblib.load(file_name)

def make_predictions(model, X_test):
    """
    Make predictions using the trained model.

    Args:
    model (RandomForestClassifier): Trained model.
    X_test (np.ndarray): Test features.

    Returns:
    np.ndarray: Predicted labels for the test data.
    """
    return model.predict(X_test)

def evaluate_model(predictions, y_test):
    """
    Evaluate the model using accuracy metric.

    Args:
    predictions (np.ndarray): Predicted labels.
    y_test (np.ndarray): True labels.

    Returns:
    float: Accuracy of the model.
    """
    from sklearn.metrics import accuracy_score
    accuracy = accuracy_score(y_test, predictions)
    print(f"Accuracy: {accuracy}")
    return accuracy

def print_classification_report(y_test, y_pred):
    """
    Print the classification report for the predictions made by the model.

    Args:
    y_test (np.ndarray): True labels.
    y_pred (np.ndarray): Predicted labels.

    Returns:
    None: Outputs the classification report to the console.
    """
    report = classification_report(y_test, y_pred, zero_division=0, output_dict=True)
    df_report = pd.DataFrame(report).transpose()
    print(df_report)

def plot_data(X, y):
    """
    Plot a scatter plot of the dataset.

    Args:
    X (np.ndarray): Features of the dataset.
    y (np.ndarray): Labels of the dataset.

    Returns:
    None: Displays a scatter plot of the data.
    """
    plt.scatter(X[:, 3], X[:, 4], c=y, cmap='viridis', marker='o', edgecolor='k')
    plt.title('Visualization of Multi-Feature Blob Data')
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    plt.show()

# Example usage of the functions defined above:
# file_path = 'data.xlsx'
# df_clean = load_and_clean_data(file_path)
# data_scaled = preprocess_data(df_clean)
# data_pca = apply_pca(data_scaled)
# clusters = perform_kmeans(data_pca, n_clusters=5)
# plot_clusters(data_pca, clusters)
# model = train_random_forest(X_train, y_train)
# save_model(model, 'random_forest_model.joblib')
# loaded_model = load_model('random_forest_model.joblib')
# predictions = make_predictions(loaded_model, X_test)
# accuracy = evaluate_model(predictions, y_test)
# print_classification_report(y_test, predictions)

