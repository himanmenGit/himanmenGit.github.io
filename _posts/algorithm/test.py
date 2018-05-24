def solution(n):
    answer = list(range(n + 1))
    for i in range(2, n + 1):
        if answer[i] == 0:
            continue
        for j in range(i + i, n + 1, i):
            answer[j] = 0
    return len(list(set(answer))[2:])


print(solution(20))
