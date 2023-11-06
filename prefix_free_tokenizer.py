class TrieNode:
    def __init__(self):
        self.children = {}
        self.count = 0
        self.parent = None
        self.depth = 0

class Trie:
    def __init__(self, symbols):
        self.root = TrieNode()
        self.symbols = set(symbols)

    def insert(self, word):
        node = self.root
        for char in word:
            node.count += 1
            if char not in node.children:
                node.children[char] = TrieNode()
                node.children[char].parent = node
                node.children[char].depth = node.depth + 1
            node = node.children[char]

    def make_complete(self):
        def complete(node):
            missing_symbols = self.symbols - set(node.children.keys())
            for symbol in missing_symbols:
                dummy_node = TrieNode()
                dummy_node.parent = node
                dummy_node.depth = node.depth + 1
                node.children[symbol] = dummy_node
            for child in node.children.values():
                if child.children:  # Corrected termination condition
                    complete(child)

        complete(self.root)

    def prune(self, m):
        
        self.make_complete()

        def collect_groups(node, groups):
            l = len(node.children)
            if l == len(self.symbols):
                groups.append(node)
                for child in node.children.values():
                    collect_groups(child, groups)
            elif l == 0:
                pass
            else:
                print(node.children)
                raise Exception("Tree is not complete")
        
        def count_leaf_nodes():
            leaf_nodes = []

            def collect_leaf_nodes(node):
                if not node.children:
                    leaf_nodes.append(node)
                else:
                    for child in node.children.values():
                        collect_leaf_nodes(child)

            collect_leaf_nodes(self.root)
            return len(leaf_nodes)
        
        def prune_group(group):
            for child in group.children.values():
                assert len(child.children) == 0
            group.children = {}

        self.make_complete()

        groups = []
        collect_groups(self.root, groups)
        groups.sort(key=lambda grp: (grp.count, -grp.depth))
        
        leaf_count = count_leaf_nodes()

        while leaf_count > m and groups:
            group_to_prune = groups.pop(0)
            print(group_to_prune.depth, group_to_prune.count, len(group_to_prune.children))
            prune_group(group_to_prune)
            leaf_count = leaf_count - len(self.symbols) + 1
            #print(leaf_count,m)

    def dump_sequences(self):
        def dfs(node, path, sequences):
            if node != self.root and not node.children:
                sequences.append(path)
            for char, child in node.children.items():
                dfs(child, path + char, sequences)

        sequences = []
        dfs(self.root, "", sequences)
        return sequences

# Example usage
symbols = {'h', 'e', 'l', 'o', 'a', 'v', 'y', 'n'}
trie = Trie(symbols)
trie.insert("hello")
trie.insert("hell")
trie.insert("heaven")
trie.insert("heavy")
trie.insert("hello")

print("A",trie.root.count)
trie.prune(30)  # Prune the trie to have close to 5 leaf nodes without exceeding
sequences = trie.dump_sequences()  # Dump all sequences
print(len(sequences))
print(sequences)  # Print the dumped sequences

