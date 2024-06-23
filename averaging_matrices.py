# Authors:
# Bartosz Kowalski 318382
# Dominika Wyszyńska 318409

import os
import numpy as np

def parse_confusion_matrix(file_content):
    lines = file_content.splitlines()
    start_idx = lines.index('Confusion matrix:') + 1
    matrix_dict = {}
    current_class = None
    for line in lines[start_idx:]:
        line = line.strip()
        if not line:
            continue
        if line.endswith(':'):
            current_class = line[:-1]
            matrix_dict[current_class] = {}
        else:
            parts = line.split(':')
            key = parts[0].strip()
            value = int(parts[1].strip())
            matrix_dict[current_class][key] = value
    return matrix_dict

def average_confusion_matrices(matrices):
    all_classes = set()
    for matrix in matrices:
        all_classes.update(matrix.keys())
    
    all_classes = sorted(all_classes)
    class_to_idx = {cls: idx for idx, cls in enumerate(all_classes)}
    
    matrix_sum = np.zeros((len(all_classes), len(all_classes)), dtype=float)
    
    for matrix in matrices:
        for row_class, row_values in matrix.items():
            row_idx = class_to_idx[row_class]
            for col_class, count in row_values.items():
                col_idx = class_to_idx[col_class]
                matrix_sum[row_idx, col_idx] += count
    
    num_matrices = len(matrices)
    if num_matrices > 0:
        average_matrix = matrix_sum / num_matrices
    else:
        average_matrix = matrix_sum
    return average_matrix, all_classes

def format_matrix_to_string(matrix, classes):
    lines = ["Confusion matrix:"]
    for i, row_class in enumerate(classes):
        lines.append(f"{row_class}:")
        for j, col_class in enumerate(classes):
            lines.append(f"\t{col_class}: {matrix[i, j]:.2f}")
    return "\n".join(lines)

def main(folder_path):
    matrices = []
    
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            with open(os.path.join(folder_path, filename), 'r') as file:
                content = file.read()
                matrix = parse_confusion_matrix(content)
                matrices.append(matrix)
    
    avg_matrix, classes = average_confusion_matrices(matrices)
    print(f"Average matrix:\n{avg_matrix}")
    result_string = format_matrix_to_string(avg_matrix, classes)
    
    with open('confusion_matrix_avg.txt', 'w') as file:
        file.write(result_string)
    
    print(result_string)

if __name__ == "__main__":
    folder_path = '.' 
    main(folder_path)
