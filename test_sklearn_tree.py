# Authors:
# Bartosz Kowalski 318382
# Dominika Wyszyńska 318409

import pandas as pd
import numpy as np
import sys
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, confusion_matrix

def main(file_name, separator, run_id):
    data = pd.read_csv(file_name, sep=separator)
    X = data.iloc[:, :-1]
    y = data.iloc[:, -1]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42)
    clf = DecisionTreeClassifier(criterion='entropy')
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    conf_matrix = confusion_matrix(y_test, y_pred)
    with open(f"results_{run_id}.txt", 'w') as f:
        f.write(f"Plik: {file_name}\n")
        f.write(f"Separator: {separator}\n")
        f.write(f"Run ID: {run_id}\n")
        f.write(f"Accuracy: {accuracy*100}\n")
        f.write("Confusion Matrix:\n")
        np.savetxt(f, conf_matrix, fmt='%d')

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python program.py <file_name> <separator> <run_id>")
    else:
        file_name = sys.argv[1]
        separator = sys.argv[2]
        run_id = sys.argv[3]
        main(file_name, separator, run_id)
