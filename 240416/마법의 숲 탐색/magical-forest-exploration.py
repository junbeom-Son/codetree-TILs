from collections import deque

downX, downY = [1, 2, 1], [-1, 0, 1]
leftX, leftY = [1, 0, -1], [-1, -2, -1]
rightX, rightY = [1, 0, -1], [1, 2, 1]
ux, uy = [-1, 0, 1, 0, 0], [0, 0, 0, -1, 1]
exitX, exitY = [-1, 0, 1, 0], [0, 1, 0, -1]
dx, dy = [-1, 1, 0, 0], [0, 0, -1, 1]

def canGoDown(row, col):
    if row == R - 2:
        return False
    for i in range(3):
        dx, dy = row + downX[i], col + downY[i]
        if 0 <= dx and forest[dx][dy] != 0:
            return False
    return True

def canGoLeft(row, col):
    if col == 1:
        return False
    for i in range(3):
        dx, dy = row + leftX[i], col + leftY[i]
        if 0 <= dx and forest[dx][dy] != 0:
            return False
    return canGoDown(row, col - 1)

def canGoRight(row, col):
    if col == C - 2:
        return False
    for i in range(3):
        dx, dy = row + rightX[i], col + rightY[i]
        if 0 <= dx and forest[dx][dy] != 0:
            return False
    return canGoDown(row, col + 1)

def setUFO(number, row, col, direction):
    for i in range(5):
        dx, dy = row + ux[i], col + uy[i]
        forest[dx][dy] = number

    topPositions[col - 1] = row
    topPositions[col] = row - 1
    topPositions[col + 1] = row
    directions[number] = direction
    exits[number] = [row + exitX[direction], col + exitY[direction]]

def clearForest():
    exits.clear()
    directions.clear()
    for i in range(R):
        for j in range(C):
            forest[i][j] = 0
    for i in range(C):
        topPositions[i] = R

def dropUFO(number, col, direction):
    row = min(topPositions[col] - 2, min(topPositions[col - 1] - 1, topPositions[col + 1] - 1))
    while True:
        if canGoDown(row, col):
            row += 1
        elif canGoLeft(row, col):
            row += 1
            col -= 1
            direction = (direction - 1 + 4) % 4
        elif canGoRight(row,  col):
            row += 1
            col += 1
            direction = (direction + 1) % 4
            continue
        else:
            break

    if row <= 0:
        clearForest()
        return

    setUFO(number, row, col, direction)

def calculateScore(number):
    if not directions:
        return 0
    score = getBaseScore(number)
    if score == R:
        return score
    included = set()
    included.add(number)
    x, y = exits[number]
    queue = deque()
    queue.append(number)
    while queue:
        number = queue.popleft()
        x, y = exits[number]
        score = max(score, getBaseScore(number))
        if score == R:
            break
        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]
            if 0 <= nx < R and 0 <= ny < C and forest[nx][ny] != 0 and forest[nx][ny] not in included:
                queue.append(forest[nx][ny])
                included.add(number)

    return score

def getBaseScore(number):
    score = exits[number][0] + 1
    if directions[number] == 0:
        score += 2
    elif directions[number] in (1, 3):
        score += 1
    return score


R, C, K = map(int, input().split())
UFOs = [[]] + [list(map(int, input().split())) for _ in range(K)]
forest = [[0 for _ in range(C)] for _ in range(R)]
topPositions = [R] * C
directions = dict()
exits = dict()
score = 0
for i in range(1, K + 1):
    col, direction = UFOs[i]
    dropUFO(i, col - 1, direction)
    score += calculateScore(i)

print(score)