import timeit
import matplotlib.pyplot as plt
from functools import lru_cache


@lru_cache(maxsize=None)
def fibonacci_lru(n):
    if n < 2:
        return n
    return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)

class SplayNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None

class SplayTree:
    def __init__(self):
        self.root = None

    def _splay(self, root, key):
        if root is None or root.key == key:
            return root
        
        if key < root.key:
            if root.left is None:
                return root
            if key < root.left.key:
                root.left.left = self._splay(root.left.left, key)
                root = self._rotate_right(root)
            elif key > root.left.key:
                root.left.right = self._splay(root.left.right, key)
                if root.left.right is not None:
                    root.left = self._rotate_left(root.left)
            return root if root.left is None else self._rotate_right(root)
        
        else:
            if root.right is None:
                return root
            if key > root.right.key:
                root.right.right = self._splay(root.right.right, key)
                root = self._rotate_left(root)
            elif key < root.right.key:
                root.right.left = self._splay(root.right.left, key)
                if root.right.left is not None:
                    root.right = self._rotate_right(root.right)
            return root if root.right is None else self._rotate_left(root)
    
    def _rotate_left(self, node):
        temp = node.right
        node.right = temp.left
        temp.left = node
        return temp
    
    def _rotate_right(self, node):
        temp = node.left
        node.left = temp.right
        temp.right = node
        return temp

    def insert(self, key, value):
        if self.root is None:
            self.root = SplayNode(key, value)
            return
        self.root = self._splay(self.root, key)
        if self.root.key == key:
            self.root.value = value
            return
        node = SplayNode(key, value)
        if key < self.root.key:
            node.right = self.root
            node.left = self.root.left
            self.root.left = None
        else:
            node.left = self.root
            node.right = self.root.right
            self.root.right = None
        self.root = node
    
    def search(self, key):
        self.root = self._splay(self.root, key)
        return self.root.value if self.root and self.root.key == key else None

def fibonacci_splay(n, tree):
    if n < 2:
        return n
    cached_result = tree.search(n)
    if cached_result is not None:
        return cached_result
    result = fibonacci_splay(n - 1, tree) + fibonacci_splay(n - 2, tree)
    tree.insert(n, result)
    return result


n_values = list(range(0, 951, 50))
lru_times = []
splay_times = []

splay_tree = SplayTree()

for n in n_values:
    lru_time = timeit.timeit(lambda: fibonacci_lru(n), number=5) / 5
    splay_time = timeit.timeit(lambda: fibonacci_splay(n, splay_tree), number=5) / 5
    lru_times.append(lru_time)
    splay_times.append(splay_time)


print("n         LRU Cache Time (s)  Splay Tree Time (s)")
print("--------------------------------------------------")
for i in range(len(n_values)):
    print(f"{n_values[i]:<10}{lru_times[i]:<20.8f}{splay_times[i]:<20.8f}")


plt.figure(figsize=(10, 5))
plt.plot(n_values, lru_times, label="LRU Cache", marker="o")
plt.plot(n_values, splay_times, label="Splay Tree", marker="s")
plt.xlabel("n (номер числа Фібоначчі)")
plt.ylabel("Час виконання (с)")
plt.title("Порівняння продуктивності обчислення чисел Фібоначчі")
plt.legend()
plt.grid()
plt.show()