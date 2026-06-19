# pipeline/evaluate.py
import joblib
from sklearn.metrics import accuracy_score, classification_report
from .data_preprocessing import load_and_preprocess
from .config import MODEL_PATH

def evaluate():
    X_train, X_test, y_train, y_test = load_and_preprocess()

    model = joblib.load(MODEL_PATH)

    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)

    print("Accuracy:", accuracy)
    print("\nClassification Report:\n", report)

if __name__ == "__main__":
    evaluate()