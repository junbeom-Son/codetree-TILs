from collections import deque
N, M, P, C, D = map(int, input().split())
dx = [-1, 0, 1, 0, -1, -1, 1, 1]
dy = [0, 1, 0, -1, -1, 1, -1, 1]

def moveSanta(number, turn):
    santaNextTurn[number] = turn + 1
    sr, sc = santaPositions[number]
    distance = getDistance(rr, rc, sr, sc)
    csx, csy = -1, -1
    direction = -1
    for i in range(4):
        nsx = sr + dx[i]
        nsy = sc + dy[i]
        if inRange(nsx, nsy) and board[nsx][nsy] == 0: # 산타가 없는 칸인 경우
            nextDistance = getDistance(rr, rc, nsx, nsy)
            if distance > nextDistance: # 다음 거리가 가까울 때만
                csx, csy = nsx, nsy
                distance = nextDistance
                direction = i
    if csx == -1 and csy == -1: # 갈 수 있는 곳이 없으면 패스
        return
    board[sr][sc] = 0
    if csx != rr or csy != rc: # 루돌프가 있는 곳이 아니라면
        board[csx][csy] = number
        santaPositions[number] = [csx, csy]
        return

    santaNextTurn[number] = turn + 2
    santaScores[number] += D
    oppositeDirection = (direction + 2) % 4
    sr, sc = csx + (dx[oppositeDirection] * D), csy + (dy[oppositeDirection] * D)

    # 격자 밖이든, 산타 움직임(상호작용이 없어도 interact method에서 처리)
    interact(number, sr, sc, oppositeDirection)



def moveRDF(turn):
    global rr, rc
    cr, cc = findClosestSanta()
    distance = getDistance(rr, rc, cr, cc)
    rnx, rny = rr, rc
    direction = -1
    for i in range(8):
        nx = rr + dx[i]
        ny = rc + dy[i]
        nextDistance = getDistance(nx, ny, cr, cc)
        if distance > nextDistance:
            rnx, rny = nx, ny
            distance = nextDistance
            direction = i

    if board[rnx][rny] != 0:  # 루돌프가 움직이는 자리에 산타가 있는 경우
        santaNumber = board[rnx][rny]
        santaNextTurn[santaNumber] = turn + 2
        snx, sny = rnx + (dx[direction] * C), rny + (dy[direction] * C) # 산타의 다음 위치
        santaScores[santaNumber] += C
        board[rnx][rny] = 0 # 기존 위치에서는 없어짐
        if not inRange(snx, sny): # 산타가 밀려나서 밖으로 나가면 아웃
            deadSantaNumbers.add(santaNumber)
        else: # 게임판 안에 아직 남아있어 상호작용이 일어날 수도 있음
            interact(santaNumber, snx, sny, direction)
    rr, rc = rnx, rny

def interact(santaNumber, x, y, direction):
    if not inRange(x, y):
        deadSantaNumbers.add(santaNumber)
        return
    if board[x][y] != 0: # 상호작용이 일어나는 경우
        interact(board[x][y], x + dx[direction], y + dy[direction], direction)

    santaPositions[santaNumber] = [x, y]
    board[x][y] = santaNumber

def findClosestSanta():
    closestDistance = 10000000
    cr, cc = -1, -1
    for santa in santas:
        r, c = santaPositions[santa]
        distance = getDistance(rr, rc, r, c)
        if distance < closestDistance:
            closestDistance = distance
            cr, cc = r, c
        elif distance == closestDistance:
            if r > cr:
                cr, cc = r, c
            elif r == cr and c > cc:
                cr, cc = r, c

    return cr, cc

def getDistance(r1, c1, r2, c2):
    d1 = (r1 - r2) * (r1 - r2)
    d2 = (c1 - c2) * (c1 - c2)
    return d1 + d2

def inRange(x, y):
    if 1 <= x <= N and 1 <= y <= N:
        return True
    return False

board = [[0 for _ in range(N + 1)] for _ in range(N + 1)]
rr, rc = map(int, input().split())
santaPositions = [[] for _ in range(P + 1)]
deadSantaNumbers = set()
santaScores = [0] * (P + 1)
santaNextTurn = [1] * (P + 1)
for _ in range(P):
    number, r, c = map(int, input().split())
    santaPositions[number] = [r, c]
    board[r][c] = number

santas = deque()
for i in range(1, P + 1):
    santas.append(i)

for i in range(1, M + 1):
    if not santas:
        break
    moveRDF(i)
    newSantas = deque()
    while santas:
        santa = santas.popleft()
        if santa in deadSantaNumbers: # 다른 조건에 의해 죽은 산타라면
            continue
        if santaNextTurn[santa] == i: # 기절하지 않았으면 움직인다.
            moveSanta(santa, i)
        if santa not in deadSantaNumbers: # 살아있으면 다시 넣어준다.
            newSantas.append(santa)

    while newSantas:
        santa = newSantas.popleft()
        if santa not in deadSantaNumbers:
            santas.append(santa)
            santaScores[santa] += 1

print(' '.join(map(str, santaScores[1:])))