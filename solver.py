#%%
# (x1 V ~x2) ^ (~x3 V x4), input = p1n2n3p4
# node numberings: x1 -> 1, ..., x4 -> 4, ~x1 -> 5, ..., ~x4 -> 8
NUM_VARS = 4

def solve_2sat(f):
    num_nodes = 2 * NUM_VARS + 1  # include dummy 0 node
    neighbors = [set() for _ in range(num_nodes)]

    if len(f) % 4 != 0:
        raise Exception(f'{f} not valid.')

    def str_to_node(s):
        add = 0 if s[0] == 'p' else NUM_VARS
        return int(s[1]) + add

    def negate_node(n):
        if n <= NUM_VARS:
            return n + NUM_VARS
        else:
            return 1 + ((n + NUM_VARS) % num_nodes)

    for i in range(0, len(f), 4):
        n1 = str_to_node(f[i : i + 2])
        n2 = str_to_node(f[i + 2 : i + 4])

        if negate_node(n1) != n2:
            neighbors[negate_node(n1)].add(n2)

        if negate_node(n2) != n1:
            neighbors[negate_node(n2)].add(n1)

    def reverse_graph(neighbors):
        rev_neighbors = [set() for _ in range(num_nodes)]

        for i in range(1, num_nodes):
            for n in neighbors[i]:
                rev_neighbors[n].add(i)

        return rev_neighbors

    def dfs_postorder(neighbors, ord_sources=None):
        count = 0
        pr_num = [-1] * num_nodes
        po_num = [-1] * num_nodes
        seen = set()
        sccs = []

        def dfs_(node, neighbors, pr_num, po_num, seen, seen_cc, count):
            seen.add(node)
            seen_cc.add(node)
            pr_num[node] = count
            count += 1

            for next_node in neighbors[node]:
                if next_node not in seen:
                    count = dfs_(next_node, neighbors, pr_num, po_num, seen, seen_cc, count)

            po_num[node] = count
            return count + 1

        ord_sources = range(1, num_nodes) if ord_sources is None else ord_sources

        for source in ord_sources:
            if source not in seen:
                seen_cc = set()
                sccs.append(seen_cc)
                count = dfs_(source, neighbors, pr_num, po_num, seen, seen_cc, count)

        return po_num, sccs

    rev_neighbors = reverse_graph(neighbors)
    po_num, _ = dfs_postorder(rev_neighbors)

    sorted_nodes = [n for (n, po) in sorted([t for t in enumerate(po_num)], key=lambda t: t[1], reverse=True)]
    _, sccs = dfs_postorder(neighbors, ord_sources = sorted_nodes)

    unsat = set()
    for scc in sccs:
        for n in scc:
            if negate_node(n) in scc:
                if n <= NUM_VARS:
                    unsat.add(n)

    if len(unsat) == 0:
        assignments = [-1] * num_nodes

        for scc in sccs:
            for n in scc:
                if assignments[n] == -1 and assignments[negate_node(n)] == -1:
                    assignments[n] = 1
                    assignments[negate_node(n)] = 0

        print(f'Satisfiable assignment: {assignments[1:NUM_VARS + 1]}')
    else:
        print(f'Unsatisfiable variables: {unsat}')

# %%
solve_2sat('p1n2n1n3p1p2n3p4n1p4')

# %%
