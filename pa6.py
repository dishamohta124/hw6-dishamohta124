#QUESTION 1

def make_change(total):
    coins = [1, 5, 10, 25, 100]
    def find_combinations(amount, current_combination, start_index, results):
        if amount == 0:
            results.append(current_combination.copy())
            return
        if amount < 0:
            return
        for i in range(start_index, len(coins)):
            current_combination.append(coins[i])
            find_combinations(amount - coins[i], current_combination, i, results)
            current_combination.pop()  
    
    results = []
    find_combinations(total, [], 0, results)
    return results

total = 10
combinations = make_change(total)
print(f"Total combinations for {total} cents are: {len(combinations)}")
for combo in combinations:
    print(combo)

#QUESTION 2
    
def dict_filter(checker, d):
    result = {}
    for key, value in d.items():
        if checker(key, value):
            result[key] = value
    return result

def checker(name, abbrev):
    return abbrev[0] == "I" and name[1] == "l"


#QUESTION 3

class KVTree:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.children = []

    def add_child(self, child):
        self.children.append(child)

def treemap(func, node):
    new_key, new_value = func(node.key, node.value)
    node.key = new_key
    node.value = new_value
    
    for child in node.children:
        treemap(func, child)

samplekv = KVTree("us", 4.6)
pa = KVTree("pa", 1.9)
samplekv.add_child(pa)
pa.add_child(KVTree("Pittsburgh", 0.3))
pa.add_child(KVTree("Philadelphia", 1.6))
il = KVTree("il", 2.7)
samplekv.add_child(il)
il.add_child(KVTree("Chicago", 2.7))

transform = lambda x, y: (x.upper(), y * 1000000)

treemap(transform, samplekv)

def print_tree(node, level=0):
    print('  ' * level + f"{node.key}: {node.value}")
    for child in node.children:
        print_tree(child, level + 1)

print_tree(samplekv)

#QUESTION 4
          
class DTree:
    def __init__(self, variable, threshold, lessequal, greater, outcome):
        # Validation to ensure proper usage of arguments
        if (variable is not None and threshold is not None and lessequal is not None and greater is not None and outcome is None) or \
           (variable is None and threshold is None and lessequal is None and greater is None and outcome is not None):
            self.variable = variable
            self.threshold = threshold
            self.lessequal = lessequal
            self.greater = greater
            self.outcome = outcome
        else:
            raise ValueError("Invalid parameters: either provide variable, threshold, lessequal, and greater, or provide outcome alone.")
    
    def tuple_atleast(self):
        # This method determines the minimum size of the tuple needed to make a decision
        if self.variable is None:
            return 0
        max_index = self.variable + 1  # Accounts for zero-based indexing
        if self.lessequal is not None:
            max_index = max(max_index, self.lessequal.tuple_atleast())
        if self.greater is not None:
            max_index = max(max_index, self.greater.tuple_atleast())
        return max_index

    def find_outcome(self, observation):
        # This method navigates the tree based on the observation tuple and returns the outcome
        if self.outcome is not None:
            return self.outcome
        current_value = observation[self.variable]
        if current_value <= self.threshold:
            return self.lessequal.find_outcome(observation)
        else:
            return self.greater.find_outcome(observation)

    def no_repeats(self):
        # Wrapper method that calls a recursive helper with no initial variables seen
        return self._no_repeats_helper(set())

    def _no_repeats_helper(self, seen):
        # Recursive helper that checks for repeated variable queries in any decision path
        if self.variable in seen:
            return False
        if self.variable is not None:
            seen.add(self.variable)
        lessequal_valid = True if self.lessequal is None else self.lessequal._no_repeats_helper(seen.copy())
        greater_valid = True if self.greater is None else self.greater._no_repeats_helper(seen.copy())
        return lessequal_valid and greater_valid

# Example Usage:
root = DTree(0, 66,
             DTree(2, 10,
                   DTree(None, None, None, None, "walk"),
                   DTree(None, None, None, None, "stay home"),
                   None),
             DTree(None, None, None, None, "stay home"),
             None)

print("Tuple atleast needed:", root.tuple_atleast())
print("Outcome for [67, 50, 5]:", root.find_outcome([67, 50, 5]))
print("Outcome for [65, 50, 11]:", root.find_outcome([65, 50, 11]))
print("No repeats in tree:", root.no_repeats())

          
