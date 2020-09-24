from typing import List
from collections import deque

def colorize_bfs(
    groups: List[List[int]],
    grid: List[List[int]],
    row: int, col: int,
    group_id: int
):
    rows = len(grid)
    cols = len(grid[0])
    start_value = grid[row][col]
    queue = deque([(row, col)])
    visited = {(row, col)}

    while queue:
        row, col = queue.popleft()
        groups[row][col] = group_id

        for dr, dc in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            next_row = row + dr
            next_col = col + dc
            if (next_row >= 0 and next_row < rows
                    and next_col >= 0 and next_col < cols
                    and (next_row, next_col) not in visited
                    and grid[next_row][next_col] == start_value):
                visited.add((next_row, next_col))
                queue.append((next_row, next_col))

def colorize_group(grid: List[List[int]]) -> List[List[int]]:
    rows = len(grid)
    cols = len(grid[0])

    groups = [[0] * cols for row in range(rows)]
    group_id = 1

    for row in range(rows):
        for col in range(cols):
            if groups[row][col] == 0:
                colorize_bfs(groups, grid, row, col, group_id)
                group_id += 1

    return groups


def to_zero_index(raw: str) -> int:
    return int(raw) - 1


if __name__ == '__main__':
    rows, cols = map(int, input().split())
    grid = []
    for row in range(rows):
        grid.append(list(map(int, input())))

    groups = colorize_group(grid)

    total_query = int(input())

    for q in range(total_query):
        r1, c1, r2, c2 = map(to_zero_index, input().split())
        if grid[r1][c1] != grid[r2][c2]:
            print('neither')
            continue
        if groups[r1][c1] == groups[r2][c2]:
            print('binary' if grid[r1][c1] == 0 else 'decimal')
        else:
            print('neither')