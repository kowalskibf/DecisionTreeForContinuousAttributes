# Authors:
# Bartosz Kowalski 318382
# Dominika Wyszyńska 318409

from DecisionTree import *
import sys
import random
from datetime import datetime
from DecisionTreeVariance import DecisionTreeMinimizingVariance

ALL_POSSIBLE = 0
EVEN_DISTRIBUTION = 1
MINIMIZING_VARIANCE = 2

def main(file_name, separator, id):
    attributes, records = read_data(file_name, separator=separator)
    random.shuffle(records)
    split = int(0.4 * len(records))
    training_data = records[:split]
    testing_data = records[split:]
    dt = DecisionTreeMinimizingVariance(attributes, training_data)
    dt.build_tree()
    
    actual = [rec[attributes[-1].name] for rec in testing_data]
    predicted = [dt.predict_result(rec) for rec in testing_data]
    classes = list(set(actual + predicted))
    matrix = confusion_matrix(actual, predicted, classes)
    accuracy = sum(matrix[key][key] for key in matrix.keys()) / len(testing_data) * 100
    print(f'Accuracy: {accuracy}%')
    
    file_path = f'V_80-20_wynik_{file_name}_{id}_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.txt'
    file = open(file_path, 'w')
    file.write(f'File: {file_name}\n\n')
    file.write(str(dt))
    
    if not os.path.isfile(file_path):
        print(f"Failed to create file: {file_path}")
    else:
        print(f"Decision tree saved to {file_path}")
        
    result_attribute = attributes[-1]
    correct = 0
    for rec in testing_data:
        if dt.predict_result(rec) == rec[result_attribute.name]:
            correct += 1
    accuracy = correct / len(testing_data) * 100
    file.write(f'\n\nOverall accuracy: {accuracy}%')
    file.write(f'\n\nConfusion matrix:\n')
    for true_class in classes:
            file.write(f'{true_class}:\n')
            for predicted_class in classes:
                file.write(f'\t{predicted_class}: {matrix[true_class][predicted_class]}\n')
    
    file.close()
    del dt, attributes, records, training_data, testing_data


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python test.py <file_name> <separator>")
        sys.exit(1)
    
    file_name = sys.argv[1]
    separator = sys.argv[2]
    id = int(sys.argv[3])
    main(file_name, separator, id)
