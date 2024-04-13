import heapq

# print(pqByDomain)
# value = heapq.heappop(pqByDomain['codetree.ai'])
# print(value) (우선순위, (시간, 문제번호)
# print(value[0]) 우선순위
# print(value[1]) (시간, 문제번호)

INF = 10000000
pqByDomain = dict()
numbersByDomain = dict()
machines = []
onProcessByDomain = dict()
onProcessByMachineNumber = dict()
lastTerminatedTasks = dict()

def extractUrl(url):
    domain, number = url.split('/')
    return domain, int(number)

def getTopPriorityTask(includedDomains):
    topPriority = INF
    minTime = INF
    problemNumber = INF
    selectedDomain = ''
    for domain in pqByDomain:
        if domain in includedDomains:
            continue
        priority, info = heapq.heappop(pqByDomain[domain])
        time, number = info
        heapq.heappush(pqByDomain[domain], (priority, info))
        if priority < topPriority or (priority == topPriority and time < minTime):
            topPriority = priority
            minTime = time
            problemNumber = number
            selectedDomain = domain

    if topPriority != INF:
        heapq.heappop(pqByDomain[selectedDomain])
        numbersByDomain[selectedDomain].remove(problemNumber)
        if not numbersByDomain[selectedDomain]:
            del pqByDomain[selectedDomain]
            del numbersByDomain[selectedDomain]

    return selectedDomain, problemNumber

def init(command):
    N = int(command[1])
    for i in range(1, N + 1):
        machines.append(i)
    domain, number = extractUrl(command[2])
    pqByDomain[domain] = []
    heapq.heappush(pqByDomain[domain], (1, (0, number)))
    numbersByDomain[domain] = set()
    numbersByDomain[domain].add(number)

def request(command):
    code, t, p, u = command
    t, p = int(t), int(p)
    domain, number = extractUrl(u)
    if domain not in numbersByDomain: # 해당 도메인의 요청이 없었던 경우
        numbersByDomain[domain] = set()
        pqByDomain[domain] = []

    if number not in numbersByDomain[domain]: # 해당 도메인의 문제가 이미 존재하는 경우, 추가하지 않음
        numbersByDomain[domain].add(number)
        heapq.heappush(pqByDomain[domain], (p, (t, number)))


def tryCorrection(command):
    code, t = command
    t = int(t)
    if not machines: # 쉬고 있는 채점기가 없으면 시도 X
        return
    includedDomains = set()
    for domain in onProcessByDomain: # 채점 중인 도메인 체크
        includedDomains.add(domain)

    for domain in lastTerminatedTasks: # 현재 시간 기준 시작할 수 없는 도메인 추출
        startTime = lastTerminatedTasks[domain]
        if t < startTime:
            includedDomains.add(domain)

    # 가장 우선순위 높은 문제 추출
    selectedDomain, problemNumber = getTopPriorityTask(includedDomains)
    if problemNumber == INF: # 우선순위 높은 문제가 없으면 진행 X
        return

    # 채점기 번호 추출
    machineNumber = heapq.heappop(machines)

    # 채점 중인 상태 저장
    onProcessByDomain[selectedDomain] = (machineNumber, t)
    onProcessByMachineNumber[machineNumber] = selectedDomain

def terminateCorrection(command):
    code, t, Jid = command
    t, Jid = int(t), int(Jid)
    if Jid not in onProcessByMachineNumber: # 해당 채점기가 사용중이지 않다면 무시
        return

    # 채점 중인 정보 추출 후 삭제
    domain = onProcessByMachineNumber[Jid]
    del onProcessByMachineNumber[Jid]

    startTime = onProcessByDomain[domain][1]
    del onProcessByDomain[domain]

    gap = t - startTime
    nextTime = startTime + (3 * gap)

    lastTerminatedTasks[domain] = nextTime # 해당 도메인의 다음 시작시간 업데이트
    heapq.heappush(machines, Jid) # 채점기 반환

def getCountInQueue():
    count = 0
    for domain in numbersByDomain:
        count += len(numbersByDomain[domain])
    return count

Q = int(input())
commands = [list(input().split()) for _ in range(Q)]
answers = []

for command in commands:
    commandNumber = int(command[0])
    if commandNumber == 100:
        init(command)
    elif commandNumber == 200:
        request(command)
    elif commandNumber == 300:
        tryCorrection(command)
    elif commandNumber == 400:
        terminateCorrection(command)
    elif commandNumber == 500:
        answers.append(getCountInQueue())

print('\n'.join(map(str, answers)))