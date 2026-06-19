# pipeline/train.py
from sklearn.ensemble import RandomForestClassifier
import joblib
from .data_preprocessing import load_and_preprocess
from .config import MODEL_PATH

def train():
    X_train, X_test, y_train, y_test = load_and_preprocess()

    model = RandomForestClassifier(n_estimators=20, random_state=0)
    model.fit(X_train, y_train)

    joblib.dump(model, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")

if __name__ == "__main__":
    train()