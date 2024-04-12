from collections import deque

def setNotification(c):
    if isOnNotification[c]:
        isOnNotification[c] = False
    else:
        isOnNotification[c] = True

def setPower(c, power):
    authorities[c] = power

def exchangeParents(c1, c2):
    p1, p2 = parents[c1], parents[c2]
    children[p1].remove(c1)
    children[p2].remove(c2)
    children[p1].add(c2)
    children[p2].add(c1)
    parents[c1], parents[c2] = parents[c2], parents[c1]

def getNotificationCount(c):
    queue = deque()
    for child in children[c]:
        queue.append((1, child))
    count = 0
    while queue:
        depth, number = queue.popleft()
        if not isOnNotification[number]: # 알람 설정이 꺼져 있으면 그 자식들도 전파 불가능
            continue
        if depth <= authorities[number]: # 채팅방 c 까지 알람이 도달하는 경우 카운트
            count += 1
        for child in children[number]: # 다음 자식으로 전파
            queue.append((depth + 1, child))

    return count

N, Q = map(int, input().split())
initialInput = list(map(int, input().split()))
parents = [0] + initialInput[1:(N + 1)]
authorities = [0] + initialInput[(N + 1):]
queries = [list(map(int, input().split())) for _ in range(Q - 1)]
isOnNotification = [True] * (N + 1)
children = [set() for _ in range(N + 1)]
for i in range(1, N + 1):
    children[parents[i]].add(i)

answers = []
for query in queries:
    command = query[0]
    if command == 200:
        setNotification(query[1])
    elif command == 300:
        setPower(query[1], query[2])
    elif command == 400:
        exchangeParents(query[1], query[2])
    else:
        answers.append(getNotificationCount(query[1]))

print('\n'.join(map(str, answers)))