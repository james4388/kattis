from typing import List
from collections import deque

class DisjoinSet:
    def __init__(self, size: int):
        self.parents = list(range(size))
        self.ranks = [0] * size

    def find_root(self, x: int):
        parents = self.parents
        if parents[x] != x:
            parents[x] = self.find_root(parents[x])
        return parents[x]

    def union(self, x: int, y: int):
        root_x = self.find_root(x)
        root_y = self.find_root(y)
        if root_x == root_y:
            return root_x
        ranks = self.ranks
        parents = self.parents
        if ranks[root_x] < ranks[root_y]:
            root_x, root_y = root_y, root_x
        parents[root_y] = root_x
        if ranks[root_x] == ranks[root_y]:
            ranks[root_x] += 1
        return root_x

    def connected(self, x: int, y: int):
        return self.find_root(x) == self.find_root(y)


def to_node_index(cols: int, row: int, col: int):
    return cols * row + col


def same_group(
    djset: 'DisjoinSet',
    grid: List[List[int]],
    r1: int, c1: int, r2: int, c2: int
) -> bool:
    rows = len(grid)
    cols = len(grid[0])
    src_node = to_node_index(cols, r1, c1)
    desc_node = to_node_index(cols, r2, c2)

    if djset.connected(src_node, desc_node):
        return True

    queue = deque([(r1, c1)])
    visited = {(r1, c1)}
    connected = False
    while queue:
        row, col = queue.popleft()
        if (row, col) == (r2, c2):
            connected = True

        current_node = to_node_index(cols, row, col)

        for dr, dc in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            next_row = row + dr
            next_col = col + dc
            if (next_row >= 0 and next_row < rows
                    and next_col >= 0 and next_col < cols
                    and (next_row, next_col) not in visited
                    and grid[next_row][next_col] == grid[r1][c1]):
                visited.add((next_row, next_col))
                queue.append((next_row, next_col))
                next_node = to_node_index(cols, next_row, next_col)
                djset.union(current_node, next_node)

    return connected


def to_zero_index(raw: str) -> int:
    return int(raw) - 1


if __name__ == '__main__':
    rows, cols = map(int, input().split())
    grid = []
    for row in range(rows):
        grid.append(list(map(int, input())))

    total_query = int(input())
    djset = DisjoinSet(rows * cols)
    for q in range(total_query):
        r1, c1, r2, c2 = map(to_zero_index, input().split())
        if grid[r1][c1] != grid[r2][c2]:
            print('neither')
            continue
        if same_group(djset, grid, r1, c1, r2, c2):
            print('binary' if grid[r1][c1] == 0 else 'decimal')
        else:
            print('neither')