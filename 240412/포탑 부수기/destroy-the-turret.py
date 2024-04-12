from collections import deque
import copy

dx = [0, 1, 0, -1]
dy = [1, 0, -1, 0]
neighborX = [-1, -1, -1, 0, 0, 1, 1, 1]
neighborY = [-1, 0, 1, -1, 1, -1, 0, 1]

def getTowerNumber(i, j):
    return i * M + j

def convertOneDToTwoDIndex(oneDIndex):
    return oneDIndex // M, oneDIndex % M

def updateTargetTower(i, j):
    power = towers[i][j]
    lastAttack = lastAttacks[i][j]
    rowColSum = i + j
    col = j
    return power, lastAttack, rowColSum, col, i, j

def selectAttacker():
    minPower = INF
    lastAttack = -1
    maxRowColSum = -1
    maxCol = -1
    attackerX, attackerY = -1, -1
    for aliveTower in aliveTowers:
        i, j = convertOneDToTwoDIndex(aliveTower)
        if towers[i][j] > minPower:
            continue
        if towers[i][j] < minPower:
            minPower, lastAttack, maxRowColSum, maxCol, attackerX, attackerY = updateTargetTower(i, j)
            continue
        # 이하 첫번째 조건은 동일하다고 판단

        if lastAttacks[i][j] < lastAttack:
            continue
        if lastAttacks[i][j] > lastAttack:
            minPower, lastAttack, maxRowColSum, maxCol, attackerX, attackerY = updateTargetTower(i, j)
            continue
        # 이하 두번째 조건도 동일하다고 판단

        if i + j < maxRowColSum:
            continue
        if i + j > maxRowColSum:
            minPower, lastAttack, maxRowColSum, maxCol, attackerX, attackerY = updateTargetTower(i, j)
            continue
        # 이하 세번째 조건도 동일하다고 판단

        if j < maxCol:
            continue
        if j > maxCol:
            minPower, lastAttack, maxRowColSum, maxCol, attackerX, attackerY = updateTargetTower(i, j)
    return attackerX, attackerY

def selectTarget():
    maxPower = -INF
    lastAttack = INF
    minRowColSum = INF
    minCol = INF
    targetX, targetY = -1, -1
    for aliveTower in aliveTowers:
        i, j = convertOneDToTwoDIndex(aliveTower)
        if towers[i][j] < maxPower:
            continue
        if towers[i][j] > maxPower:
            maxPower, lastAttack, minRowColSum, minCol, targetX, targetY = updateTargetTower(i, j)
            continue

        if lastAttacks[i][j] > lastAttack:
            continue
        if lastAttacks[i][j] < lastAttack:
            maxPower, lastAttack, minRowColSum, minCol, targetX, targetY = updateTargetTower(i, j)
            continue

        if i + j > minRowColSum:
            continue
        if i + j < minRowColSum:
            maxPower, lastAttack, minRowColSum, minCol, targetX, targetY = updateTargetTower(i, j)
            continue

        if j < minCol:
            maxPower, lastAttack, minRowColSum, minCol, targetX, targetY = updateTargetTower(i, j)

    return targetX, targetY

def attack(attackerX, attackerY, targetX, targetY):
    lastPath = [[[] for _ in range(M)] for _ in range(N)]
    lastPath[attackerX][attackerY] = [-1, -1]
    queue = deque()
    queue.append([attackerX, attackerY])
    while queue:
        x, y = queue.popleft()
        if x == targetX and y == targetY:
            break
        for i in range(4):
            nx = (x + dx[i] + N) % N
            ny = (y + dy[i] + M) % M
            if not lastPath[nx][ny] and towers[nx][ny] > 0:
                lastPath[nx][ny] = [x, y]
                queue.append([nx, ny])

    notRelatedTowers = copy.deepcopy(aliveTowers)
    notRelatedTowers.remove(targetX * M + targetY)
    notRelatedTowers.remove(attackerX * M + attackerY)

    fullPower = towers[attackerX][attackerY]

    towers[targetX][targetY] -= fullPower
    if towers[targetX][targetY] <= 0:
        aliveTowers.remove(targetX * M + targetY)

    if lastPath[targetX][targetY]:
        lazerAttack(attackerX, attackerY, targetX, targetY, lastPath, notRelatedTowers)
        return notRelatedTowers

    bombAttack(attackerX, attackerY, targetX, targetY, notRelatedTowers)
    return notRelatedTowers



def lazerAttack(attackerX, attackerY, targetX, targetY, lastPath, notRelatedTowers):
    halfPower = towers[attackerX][attackerY] // 2

    x, y = lastPath[targetX][targetY]
    while not (x == attackerX and y == attackerY):
        towerNumber = x * M + y
        towers[x][y] -= halfPower
        notRelatedTowers.remove(towerNumber)
        if towers[x][y] <= 0:
            aliveTowers.remove(towerNumber)
        x, y = lastPath[x][y]

    return notRelatedTowers

def bombAttack(attackerX, attackerY, targetX, targetY, notRelatedTowers):
    subTargets = set()
    halfPower = towers[attackerX][attackerY] // 2
    for i in range(8):
        nx = (targetX + neighborX[i] + N) % N
        ny = (targetY + neighborY[i] + M) % M
        if (nx == attackerX and ny == attackerY) or (nx == targetX and ny == targetY):
            continue
        number = getTowerNumber(nx, ny)
        if number not in aliveTowers:
            continue
        if number not in subTargets:
            subTargets.add(number)
            notRelatedTowers.remove(number)
            towers[nx][ny] -= halfPower
            if towers[nx][ny] <= 0:
                aliveTowers.remove(number)


INF = 10000000
N, M, K = map(int, input().split())
towers = [list(map(int, input().split())) for _ in range(N)]
lastAttacks = [[0 for _ in range(M)] for _ in range(N)]
aliveTowers = set()
for i in range(N):
    for j in range(M):
        if towers[i][j] > 0:
            aliveTowers.add(i * M + j)

handicap = N + M

for i in range(1, K + 1):
    if len(aliveTowers) == 1:
        break
    attackerX, attackerY = selectAttacker()
    lastAttacks[attackerX][attackerY] = i
    targetX, targetY = selectTarget()
    towers[attackerX][attackerY] += handicap
    notRelatedTowers = attack(attackerX, attackerY, targetX, targetY)
    for notRelatedTower in notRelatedTowers:
        i, j = convertOneDToTwoDIndex(notRelatedTower)
        towers[i][j] += 1

# 정답 출력
maxPower = -1
for aliveTower in aliveTowers:
    i, j = convertOneDToTwoDIndex(aliveTower)
    maxPower = max(maxPower, towers[i][j])

print(maxPower)