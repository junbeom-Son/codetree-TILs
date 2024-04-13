dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]

def getDistance(x, y):
    return abs(exitX - x) + abs(exitY - y)

def getNextPosition(x, y):
    minDistance = getDistance(x, y)
    nextX, nextY = x, y
    for i in range(4):
        nx = x + dx[i]
        ny = y + dy[i]
        if 0 < nx <= N and 0 < ny <= N and maze[nx][ny] == 0:
            distance = getDistance(nx, ny)
            if distance < minDistance:
                minDistance = distance
                nextX, nextY = nx, ny

    return nextX, nextY

def move():
    global players, totalDistance
    tmpPlayers = []
    while players:
        x, y = players.pop()
        nx, ny = getNextPosition(x, y)
        if x != nx or y != ny: # 이동한다면
            x, y = nx, ny
            totalDistance += 1

        if x != exitX or y != exitY: # 도착하지 않았다면 다시 리스트에 삽입
            tmpPlayers.append([x, y])

    players = tmpPlayers

def adjust(p1, p2):
    if p1 < 1:
        adjust = 1 - p1
        p1 += adjust
        p2 += adjust
    return p1, p2

def getMinSquare():
    x1, y1, x2, y2, minLength = 0, 0, N + 1, N + 1, N + 1
    for x, y in players:
        maxX, maxY = max(x, exitX), max(y, exitY)
        length = max(abs(x - exitX), abs(y - exitY))
        tx1 = maxX - length
        tx1, maxX = adjust(tx1, maxX)
        ty1 = maxY - length
        ty1, maxY = adjust(ty1, maxY)
        if length < minLength or (length == minLength and tx1 < x1) or (length == minLength and tx1 == x1 and ty1 < y1):
            x1 = tx1
            y1 = ty1
            x2 = maxX
            y2 = maxY
            minLength = length

    return x1, y1, x2, y2

def getPositionAfterRotation(x, y, x1, y1, x2, y2):
    nx = (y - y1) + x1
    ny = y2 - (x - x1)
    return nx, ny

def rotateMaze():
    global exitX, exitY
    x1, y1, x2, y2 = getMinSquare()
    length = x2 - x1 + 1
    for i in range(length):
        for j in range(length):
            tmpMaze[j + x1][y2 - i] = maze[i + x1][j + y1]

    for i in range(length):
        for j in range(length):
            maze[i + x1][j + y1] = tmpMaze[i + x1][j + y1]
            if maze[i + x1][j + y1] > 0:
                maze[i + x1][j + y1] -= 1

    for i in range(len(players)):
        x, y = players[i]
        if x1 <= x <= x2 and y1 <= y <= y2: # 회전하는 범위 안에 있으면
            x, y = getPositionAfterRotation(x, y, x1, y1, x2, y2)
            players[i] = [x, y]

    exitX, exitY = getPositionAfterRotation(exitX, exitY, x1, y1, x2, y2)

N, M, K = map(int, input().split())
maze = [[0] * (N + 1)] + [([0] + list(map(int, input().split()))) for _ in range(N)]
players = [list(map(int, input().split())) for _ in range(M)]
exitX, exitY = map(int, input().split())
tmpMaze = [[0 for _ in range(N + 1)] for _ in range(N + 1)]
totalDistance = 0
for _ in range(K):
    if not players:
        break
    move()
    if not players:
        break
    rotateMaze()

print(totalDistance)
print(exitX, exitY)