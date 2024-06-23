# Authors:
# Bartosz Kowalski 318382
# Dominika Wyszyńska 318409

import glob
import re
import statistics

def extract_accuracy_from_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        match = re.search(r'(accuracy|Accuracy):\s*([\d\.]+)', content)
        if match:
            return float(match.group(2))
    return None

def process_files_with_prefix(prefix):
    files = glob.glob(f"*{prefix}")
    accuracies = []

    for file_path in files:
        accuracy = extract_accuracy_from_file(file_path)
        if accuracy is not None:
            accuracies.append(accuracy)

    if accuracies:
        average_accuracy = statistics.mean(accuracies)
        std_dev_accuracy = statistics.stdev(accuracies)
        min_accuracy = min(accuracies)
        max_accuracy = max(accuracies)

        print(f"Średnia dokładność: {average_accuracy:.2f}%")
        print(f"Odchylenie standardowe: {std_dev_accuracy:.2f}%")
        print(f"Minimalna dokładność: {min_accuracy:.2f}%")
        print(f"Maksymalna dokładność: {max_accuracy:.2f}%")
    else:
        print("Nie znaleziono żadnych wyników dokładności w plikach.")


if __name__ == "__main__":
    process_files_with_prefix(".txt")