# Authors:
# Bartosz Kowalski 318382
# Dominika Wyszyńska 318409

from math import log
import os
import random
from Node import *
from Attribute import *


class DecisionTree:
    def __init__(self, attributes: list, records: list):
        self.attributes = attributes[:-1]
        self.result_attribute = attributes[-1]
        self.records = records
        self.root = None

    def __str__(self):
        return self.root.__str__()
    
    def __del__(self):
        del self.root, self.records, self.attributes, self.result_attribute
        print("Decision tree deleted.")

    def find_best_attribute(self, attributes, records):
        if len(attributes) == 0:
            return None
        max_gain = float("-inf")
        max_atr = None
        max_split_point = None
        i=1
        for attribute in attributes:
            print(f'Computing gain for {i} out of {len(attributes)} attributes')
            i+=1
            if attribute.continuous:
                j=1
                for split_point in (sps:=find_split_points(attribute, self.result_attribute, records)):
                    if not j%10:
                        print(f"\tComputing split point {j}/{len(sps)}")
                    j+=1
                    curr_gain = gain(self.result_attribute, records, attribute, split_point)
                    if curr_gain > max_gain:
                        max_gain = curr_gain
                        max_atr = attribute
                        max_split_point = split_point
            else:
                curr_gain = gain(self.result_attribute, records, attribute)
                if curr_gain > max_gain:
                    max_gain = curr_gain
                    max_atr = attribute
                    max_split_point = None
        return max_atr, max_split_point
    
    def build_tree_recurr(self, node:Node, attributes_left:list, records_left:list):
        if not records_left:
            node.is_terminal = True
            node.result = max(set(record[self.result_attribute.name] for record in self.records), key=self.records[0][self.result_attribute.name].count)
            return
        
        if len(set(record[self.result_attribute.name] for record in records_left)) == 1:
            node.is_terminal = True
            node.result = records_left[0][self.result_attribute.name]
            return
        
        if not attributes_left:
            node.is_terminal = True
            node.result = max(set(record[self.result_attribute.name] for record in records_left), key=records_left[0][self.result_attribute.name].count)
            return

        best_attribute, split_point = self.find_best_attribute(attributes_left, records_left)
        if best_attribute is None:
            node.is_terminal = True
            node.result = max(set(record[self.result_attribute.name] for record in records_left), key=records_left[0][self.result_attribute.name].count)
            return
        
        if best_attribute in attributes_left and (not best_attribute.continuous or (best_attribute.continuous and not find_split_points(best_attribute, self.result_attribute, records_left))):
            attributes_left.remove(best_attribute)

        if best_attribute.continuous:
            records_left_subset = [record for record in records_left if is_value_valid(record[best_attribute.name], best_attribute, "<" + str(split_point))]
            child_node = Node(best_attribute, True, "<" + str(split_point), [])
            node.branches.append(child_node)
            self.build_tree_recurr(child_node, attributes_left, records_left_subset)
            records_left_subset = [record for record in records_left if is_value_valid(record[best_attribute.name], best_attribute, ">=" + str(split_point))]
            child_node = Node(best_attribute, True, ">=" + str(split_point), [])
            node.branches.append(child_node)
            self.build_tree_recurr(child_node, attributes_left, records_left_subset)
        else:
            for best_attribute_value in best_attribute.values:
                records_left_subset = [record for record in records_left if record[best_attribute.name] == best_attribute_value]
                child_node = Node(best_attribute, False, best_attribute_value)
                node.branches.append(child_node)
                self.build_tree_recurr(child_node, attributes_left, records_left_subset)

    def build_tree(self):
        self.root = Node()
        attributes_left = self.attributes
        best_attribute, split_point = self.find_best_attribute(attributes_left, self.records)
        self.root.attribute = best_attribute
        if best_attribute in attributes_left and (not best_attribute.continuous or (best_attribute.continuous and not find_split_points(best_attribute, self.result_attribute, self.records))):
            attributes_left.remove(best_attribute)

        if best_attribute.continuous:
            records_left_subset = [record for record in self.records if is_value_valid(record[best_attribute.name], best_attribute, "<" + str(split_point))]
            child_node = Node(best_attribute, True, "<" + str(split_point), [])
            self.root.branches.append(child_node)
            self.build_tree_recurr(child_node, attributes_left, records_left_subset)
            records_left_subset = [record for record in self.records if is_value_valid(record[best_attribute.name], best_attribute, ">=" + str(split_point))]
            child_node = Node(best_attribute, True, ">=" + str(split_point), [])
            self.root.branches.append(child_node)
            self.build_tree_recurr(child_node, attributes_left, records_left_subset)
        else:
            for best_attribute_value in best_attribute.values:
                records_left_subset = [record for record in self.records if record[best_attribute.name] == best_attribute_value]
                child_node = Node(best_attribute, False, best_attribute_value)
                self.root.branches.append(child_node)
                self.build_tree_recurr(child_node, attributes_left, records_left_subset)

    def predict_result(self, record):
        return self.predict_result_recurr(record, self.root)
    
    def predict_result_recurr(self, record, node):
        if node.is_terminal:
            return node.result
        attribute = node.branches[0].attribute
        attribute_value = record[attribute.name]
        for child in node.branches:
            if is_value_valid(attribute_value, attribute, child.value):
                return self.predict_result_recurr(record, child)

def find_split_points(attribute:Attribute, result_attribute:Attribute, records:list):
    if len(records) < 2:
        return []
    sorted_records = sorted(records, key=lambda x: x[attribute.name])
    split_points = []
    for i in range(len(sorted_records)-1):
        if sorted_records[i][result_attribute.name] != sorted_records[i+1][result_attribute.name]:
            split_points.append(round((sorted_records[i][attribute.name]+sorted_records[i+1][attribute.name])/2, 6))
    return split_points

def is_value_valid(value, attribute, condition):
    if attribute.continuous:
        return eval(str(value) + condition)
    return value == condition

def entropy(result_attribute, records, existing_result_values=[], attribute=None, value=None):
    count_for_each_result = {}
    for possible_result in existing_result_values:
        count_for_each_result[possible_result] = 0
    for record in records:
        if attribute is None or value is None or is_value_valid(record[attribute.name], attribute, value):
            count_for_each_result[record[result_attribute.name]] += 1
    e = 0
    for k in count_for_each_result.keys():
        try:
            e -= count_for_each_result[k] / sum(count_for_each_result.values()) * log(count_for_each_result[k] / sum(count_for_each_result.values()))
        except:
            return 0
    return e

def gain(result_attribute, records, attribute, split_point=None):
    existing_result_values = []
    for record in records:
        v = record[result_attribute.name]
        if v not in existing_result_values:
            existing_result_values.append(v)
    e = entropy(result_attribute, records, existing_result_values)
    if attribute.continuous:
        numerator_lt = 0
        numerator_gt = 0
        for record in records:
            if is_value_valid(record[attribute.name], attribute, "<" + str(split_point)):
                numerator_lt += 1
            else:
                numerator_gt += 1
        e -= numerator_lt / len(records) * entropy(result_attribute, records, existing_result_values, attribute, "<" + str(split_point))
        e -= numerator_gt / len(records) * entropy(result_attribute, records, existing_result_values, attribute, ">=" + str(split_point))
    else:
        for value in attribute.values:
            numerator = 0
            for record in records:
                if is_value_valid(record[attribute.name], attribute, value):
                    numerator += 1
            e -= numerator / len(records) * entropy(result_attribute, records,existing_result_values, attribute, value)
    return e


def read_data(file_name, separator=";"):
    with open(file_name, 'r', encoding='utf-8') as file:
        first_line = True
        first_record = True
        attributes = []
        records = []
        for line in file.readlines():
            if first_line:
                [attributes.append(Attribute(name)) for name in line.split("\n")[0].split(separator)]
                first_line = False
                continue
            values = line.split("\n")[0].split(separator)
            if first_record:
                for i in range(len(values)):
                    try:
                        _ = float(values[i])
                        continuous = True
                    except:
                        continuous = False
                        attributes[i].values = []
                    attributes[i].continuous = continuous
                first_record = False
            for i in range(len(attributes)):
                if i == len(attributes) - 1:
                    attributes[i].continuous=False
                if not attributes[i].continuous and not attributes[i].value_included(values[i]):
                    attributes[i].values.append(values[i])
            k = [a.name for a in attributes]
            v = []
            for i in range(len(attributes)):
                try:
                    v.append(float(values[i]))
                except:
                    v.append(values[i])
            records.append(dict(zip(k,v)))
    try:
        attributes[-1].values = [str(float(x)) for x in attributes[-1].values]
    except:
        pass
    for r in records:
        try:
            r[attributes[-1].name] = str(float(r[attributes[-1].name]))
        except:
            pass
    return attributes, records


def confusion_matrix(actual, predicted, classes):
    matrix = {}
    for true_class in classes:
        matrix[true_class] = {}
        for predicted_class in classes:
            matrix[true_class][predicted_class] = 0

    for true, pred in zip(actual, predicted):
        matrix[true][pred] += 1

    return matrix

def find_split_points_uniform(attribute:Attribute, result_attribute:Attribute, records:list):
    NUM_OF_SPLIT_POINTS = 1
    if len(records) < 2:
        return []
    min_value = min(records, key=lambda x: x[attribute.name])[attribute.name]
    max_value = max(records, key=lambda x: x[attribute.name])[attribute.name]
    step_size = (max_value - min_value) / (NUM_OF_SPLIT_POINTS + 1)
    split_points = [round(min_value + i * step_size, 6) for i in range(1, NUM_OF_SPLIT_POINTS + 1)]
    return split_points


def find_split_points_uniform_min_variance(attribute:Attribute, result_attribute:Attribute, records:list):
    NUM_OF_SPLIT_POINTS = 10
    if len(records) < 2:
        return []
    min_value = min(records, key=lambda x: x[attribute.name])[attribute.name]
    max_value = max(records, key=lambda x: x[attribute.name])[attribute.name]
    step_size = (max_value - min_value) / (NUM_OF_SPLIT_POINTS + 1)
    split_points = [round(min_value + i * step_size, 6) for i in range(1, NUM_OF_SPLIT_POINTS + 1)]
    min_var = float('inf')
    best_split_point = None
    for sp in split_points:
        rec_lt = []
        sum_lt = 0
        rec_gt = []
        sum_gt = 0
        for r in records:
            if r[attribute.name] < sp:
                rec_lt.append(r)
                sum_lt += r[attribute.name]
            else:
                rec_gt.append(r)
                sum_gt += r[attribute.name]
        avg_lt = sum_lt / len(rec_lt)
        avg_gt = sum_gt / len(rec_gt)
        var_lt = 0
        var_gt = 0
        for r in rec_lt:
            var_lt += (r[attribute.name] - avg_lt)**2
        for r in rec_gt:
            var_gt += (r[attribute.name] - avg_gt)**2
        var_lt /= len(rec_lt)
        var_gt /= len(rec_gt)
        if (new_var := (len(rec_lt) / len(records)) * var_lt + (len(rec_gt) / len(records)) * var_gt) < min_var:
            min_var = new_var
            best_split_point = sp
    return [best_split_point]

