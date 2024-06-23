# Authors:
# Bartosz Kowalski 318382
# Dominika Wyszyńska 318409

from math import log
import os
import random
import Node
from Attribute import *
from DecisionTree import *


class DecisionTreeUniform(DecisionTree):
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
                for split_point in (sps:=find_split_points_uniform(attribute, self.result_attribute, records)):
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
        
        if best_attribute in attributes_left and (not best_attribute.continuous or (best_attribute.continuous and not find_split_points_uniform(best_attribute, self.result_attribute, records_left))):
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
        if best_attribute in attributes_left and (not best_attribute.continuous or (best_attribute.continuous and not find_split_points_uniform(best_attribute, self.result_attribute, self.records))):
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