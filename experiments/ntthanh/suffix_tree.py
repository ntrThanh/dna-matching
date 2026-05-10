import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from base_class import Algorithm


class Node:
    def __init__(self, start, end=-1):
        self.start = start
        self.end = end
        self.children = {}
        self.suffix_link = None
        self.suffix_index = -1

class SuffixTreeWithBacktracking(Algorithm):
    def __init__(self, name="Suffix Tree with Backtracking"):
        super().__init__(name)
        self.text = ""
        self.root = None
        self.active_node = None
        self.active_edge = -1
        self.active_length = 0
        self.remaining_suffix_count = 0
        self.leaf_end = -1
        self.size = 0

    def edge_length(self, node):
        if node == self.root:
            return 0
        end = self.leaf_end if node.end == -1 else node.end
        return end - node.start + 1

    def walk_down(self, curr_node):
        length = self.edge_length(curr_node)
        if self.active_length >= length:
            self.active_edge += length
            self.active_length -= length
            self.active_node = curr_node
            return True
        return False

    def build(self, text):
        self.text = text + "$"
        self.root = Node(-1, -1)
        self.active_node = self.root
        self.active_edge = -1
        self.active_length = 0
        self.remaining_suffix_count = 0
        self.leaf_end = -1
        self.size = len(self.text)

        self.root.suffix_link = self.root
        for i in range(self.size):
            self.extend(i)
        self.set_suffix_index()
        
    def extend(self, pos):
        self.leaf_end = pos
        self.remaining_suffix_count += 1
        last_new_node = None
        
        while self.remaining_suffix_count > 0:
            if self.active_length == 0:
                self.active_edge = pos
                
            active_char = self.text[self.active_edge]
            
            if active_char not in self.active_node.children:
                new_leaf = Node(pos)
                self.active_node.children[active_char] = new_leaf
                
                if last_new_node is not None:
                    last_new_node.suffix_link = self.active_node
                    last_new_node = None
            else:
                next_node = self.active_node.children[active_char]
                if self.walk_down(next_node):
                    continue
                    
                edge_char = self.text[next_node.start + self.active_length]
                if edge_char == self.text[pos]:
                    if last_new_node is not None and self.active_node != self.root:
                        last_new_node.suffix_link = self.active_node
                        last_new_node = None
                    self.active_length += 1
                    break
                
                split_end = next_node.start + self.active_length - 1
                split_node = Node(next_node.start, split_end)
                self.active_node.children[active_char] = split_node
                
                new_leaf = Node(pos)
                split_node.children[self.text[pos]] = new_leaf
                next_node.start += self.active_length
                split_node.children[self.text[next_node.start]] = next_node
                
                if last_new_node is not None:
                    last_new_node.suffix_link = split_node
                    
                last_new_node = split_node
                
            self.remaining_suffix_count -= 1
            if self.active_node == self.root and self.active_length > 0:
                self.active_length -= 1
                self.active_edge = pos - self.remaining_suffix_count + 1
            elif self.active_node != self.root:
                self.active_node = self.active_node.suffix_link if self.active_node.suffix_link else self.root

    def set_suffix_index(self):
        stack = [(self.root, 0, iter(self.root.children.values()))]
        while stack:
            node, label_height, children_iter = stack[-1]
            try:
                child = next(children_iter)
                stack.append((child, label_height + self.edge_length(child), iter(child.children.values())))
            except StopIteration:
                stack.pop()
                if len(node.children) == 0:
                    node.suffix_index = self.size - label_height

    def collect_leaves(self, root, results):
        stack = [root]
        while stack:
            node = stack.pop()
            if node.suffix_index != -1:
                results.add(node.suffix_index)
            stack.extend(node.children.values())

    def run(self, text, pattern, k=0):
        self.build(text)
        
        results = set()
        
        def dfs(node, pattern_idx, mismatches):
            if mismatches > k:
                return
                
            if pattern_idx == len(pattern):
                self.collect_leaves(node, results)
                return
                
            for child in node.children.values():
                edge_len = self.edge_length(child)
                edge_start = child.start
                
                curr_p_idx = pattern_idx
                curr_mismatches = mismatches
                match_failed = False
                
                for i in range(edge_len):
                    if curr_p_idx == len(pattern):
                        self.collect_leaves(child, results)
                        match_failed = True
                        break
                        
                    edge_char = self.text[edge_start + i]
                    
                    if edge_char == '$':
                        curr_mismatches += 1
                        if curr_mismatches > k:
                            match_failed = True
                            break
                        curr_p_idx += 1
                        continue
                        
                    p_char = pattern[curr_p_idx]
                    
                    if edge_char != p_char:
                        curr_mismatches += 1
                        if curr_mismatches > k:
                            match_failed = True
                            break
                            
                    curr_p_idx += 1
                    
                if not match_failed:
                    dfs(child, curr_p_idx, curr_mismatches)
                    
        dfs(self.root, 0, 0)
        return sorted(list(results))

if __name__ == '__main__':
    algo = SuffixTreeWithBacktracking()
    print("Exact Match:", algo.evaluate("GATACGA", "GA", 0))
    print("Approximate Match (k=1):", algo.evaluate("GATACGA", "GA", 1))
