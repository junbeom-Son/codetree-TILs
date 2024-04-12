dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]

rx = [0, 1, 0, -1]
ry = [1, 0, -1, 0]

def move(x, y):
    distance = abs(x - exitX) + abs(y - exitY)
    moveX, moveY = x, y
    for i in range(4):
        nx = x + dx[i]
        ny = y + dy[i]
        nDistance = abs(nx - exitX) + abs(ny - exitY)
        if 0 < nx <= N and 0 < ny <= N and maze[nx][ny] < 1 and nDistance < distance:
            distance = nDistance
            moveX, moveY = nx, ny
    return moveX, moveY

def calculateSquare(x, y):
    x2, y2 = max(x, exitX), max(y, exitY)
    length = max(abs(x - exitX), abs(y - exitY))
    x1, y1 = x2 - length, y2 - length
    return length, x1, y1, x2, y2

def getMinSquare():
    minLength, x1, y1, x2, y2 = N, N, N, N, N
    for participant in participants:
        x, y = participants[participant]
        length, tmpX1, tmpY1, tmpX2, tmpY2 = calculateSquare(x, y)
        if length < minLength or (length == minLength and tmpX1 < x1) or (length == minLength and tmpX1 == x1 and tmpY1 < y1):
            minLength = length
            x1 = tmpX1
            y1 = tmpY1
            x2 = tmpX2
            y2 = tmpY2

    return x1, y1, x2, y2

def copySquare(x, y, x1, y1, x2, y2, length, direction):
    global exitX, exitY, tmpExitX, tmpExitY
    originX, originY = x, y
    for _ in range(length):
        nx = x + rx[direction]
        ny = y + ry[direction]
        if nx < x1 or x2 < nx or ny < y1 or y2 < ny:
            direction = (direction + 1) % 4
            nx = x + rx[direction]
            ny = y + ry[direction]
        x, y = nx, ny
    tmpMaze[x][y] = maze[originX][originY]
    if originX == exitX and originY == exitY:
        tmpExitX, tmpExitY = x, y

def rotateSquare(x1, y1, x2, y2):
    global exitX, exitY, tmpExitX, tmpExitY
    originX1, originY1, originX2, originY2 = x1, y1, x2, y2
    while x1 <= x2:
        startX, startY = x1, y1
        copySquare(x1, y1, x1, y1, x2, y2, x2 - x1, 0)
        if x1 == x2:
            break
        x, y = x1, y1 + 1
        direction = 0
        while x != startX or y != startY:
            copySquare(x, y, x1, y1, x2, y2, x2 - x1, direction)
            nx = x + rx[direction]
            ny = y + ry[direction]
            if nx < x1 or x2 < nx or ny < y1 or y2 < ny:
                direction += 1
                if direction == 4:
                    break
                nx = x + rx[direction]
                ny = y + ry[direction]
            x, y = nx, ny

        x1 += 1
        y1 += 1
        x2 -= 1
        y2 -= 1

    for i in range(originX1, originX2 + 1):
        for j in range(originY1, originY2 + 1):
            maze[i][j] = tmpMaze[i][j]
            if maze[i][j] < 0:
                participants[maze[i][j]] = [i, j]
            elif maze[i][j] > 0:
                maze[i][j] -= 1
    exitX, exitY = tmpExitX, tmpExitY

N, M, K = map(int, input().split())
maze = [[0] * (N + 1)] + [([0] + list(map(int, input().split()))) for _ in range(N)]
tmpMaze = [[0 for _ in range(N + 1)] for _ in range(N + 1)]
participants = dict()
for i in range(1, M + 1):
    participants[-i] = list(map(int, input().split()))
    maze[participants[-i][0]][participants[-i][1]] = -i
exitX, exitY = map(int, input().split())
tmpExitX, tmpExitY = exitX, exitY
totalDistance = 0
for _ in range(K):
    if not participants:
        break
    escapedParticipants = []
    for number in participants:
        x, y = participants[number]
        movedX, movedY = move(x, y)
        if movedX != x or movedY != y: # 이동했으면 카운트 + 1
            totalDistance += 1
            maze[movedX][movedY], maze[x][y] = maze[x][y], maze[movedX][movedY]
            participants[number] = [movedX, movedY]
        if movedX == exitX and movedY == exitY: # 도착처리
            escapedParticipants.append(number)

    for escapedParticipant in escapedParticipants:
        del participants[escapedParticipant]

    if not participants:
        break

    x1, y1, x2, y2 = getMinSquare()

    rotateSquare(x1, y1, x2, y2)

print(totalDistance, exitX, exitY)