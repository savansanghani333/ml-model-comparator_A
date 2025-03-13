import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score

def apply_ml_models(filepath):
    df = pd.read_csv(filepath)

    # Handle missing values (fill with most frequent value)
    df.fillna(df.mode().iloc[0], inplace=True)

    # Separate features (X) and target (y)
    X = df.iloc[:, :-1]  # All columns except the last
    y = df.iloc[:, -1]   # Last column as target

    # Encode categorical labels in target variable
    if y.dtype == "object":
        y = LabelEncoder().fit_transform(y)

    # Identify categorical features
    categorical_cols = X.select_dtypes(include=['object']).columns.tolist()

    # Encode categorical features using OneHotEncoding
    if categorical_cols:
        ct = ColumnTransformer([("encoder", OneHotEncoder(handle_unknown="ignore"), categorical_cols)], remainder="passthrough")
        X = ct.fit_transform(X).toarray()  # ✅ Convert to dense array

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # List of models
    models = {
        "Logistic Regression": LogisticRegression(),
        "Decision Tree": DecisionTreeClassifier(),
        "Random Forest": RandomForestClassifier(),
        "SVM": SVC(),
        "KNN": KNeighborsClassifier(),
        "Naive Bayes": GaussianNB(),
        "Neural Network": MLPClassifier(max_iter=500)
    }

    results = {}
    best_model = None
    best_accuracy = 0

    # Train and evaluate models
    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        results[name] = round(accuracy * 100, 2)

        if accuracy > best_accuracy:
            best_accuracy = accuracy
            best_model = name

    results["Best Model"] = best_model
    results["Best Accuracy"] = round(best_accuracy * 100, 2)

    return results
