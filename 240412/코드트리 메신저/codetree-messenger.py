from collections import deque

def setNotificationCounts(number):
    for child in children[number]:
        setNotificationCounts(child)
    notificationCounts[number][authorities[number]] = notificationCounts[number].get(authorities[number], 0) + 1
    parent = parents[number]
    for depth in notificationCounts[number]:
        if depth != 0:
            notificationCounts[parent][depth - 1] = notificationCounts[parent].get(depth - 1, 0) + notificationCounts[number][depth]

def effectNotificationCounts(c, number, depth, value):
    for reachDepth in notificationCounts[c]:
        if reachDepth >= depth:
            notificationCounts[number][reachDepth - depth] = notificationCounts[number].get(reachDepth - depth, 0) + (notificationCounts[c][reachDepth] * value)
    if number > 0 and isOnNotification[number]:
        effectNotificationCounts(c, parents[number], depth + 1, value)

def setNotification(c):
    if isOnNotification[c]:
        isOnNotification[c] = False
        effectNotificationCounts(c, parents[c], 1, -1)
    else:
        isOnNotification[c] = True
        effectNotificationCounts(c, parents[c], 1, 1)

def setPower(c, power):
    originalPower = authorities[c]
    number = c
    if not isOnNotification[c]:
        authorities[c] = power
        return
    for depth in range(originalPower, -1, -1):
        if not isOnNotification[number]:
            break
        notificationCounts[number][depth] -= 1
        if number == 0:
            break
        number = parents[number]
    authorities[c] = power
    number = c
    for depth in range(power, -1, -1):
        if not isOnNotification[number]:
            break
        notificationCounts[number][depth] = notificationCounts[number].get(depth, 0) + 1
        if number == 0:
            break
        number = parents[number]

def exchangeParents(c1, c2):
    if parents[c1] == parents[c2]:
        return
    if isOnNotification[c1]:
        effectNotificationCounts(c1, parents[c1], 1, -1)
        effectNotificationCounts(c1, parents[c2], 1, 1)
    if isOnNotification[c2]:
        effectNotificationCounts(c2, parents[c1], 1, 1)
        effectNotificationCounts(c2, parents[c2], 1, -1)
    parents[c1], parents[c2] = parents[c2], parents[c1]

def getNotificationCount(c):
    count = 0
    for key in notificationCounts[c]:
        count += notificationCounts[c][key]

    return count - 1

N, Q = map(int, input().split())
initialInput = list(map(int, input().split()))
parents = [0] + initialInput[1:(N + 1)]
authorities = [0] + initialInput[(N + 1):]
queries = [list(map(int, input().split())) for _ in range(Q - 1)]
isOnNotification = [True] * (N + 1)
children = [set() for _ in range(N + 1)]
notificationCounts = [dict() for _ in range(N + 1)]
for i in range(1, N + 1):
    children[parents[i]].add(i)

for child in children[0]:
    setNotificationCounts(child)

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