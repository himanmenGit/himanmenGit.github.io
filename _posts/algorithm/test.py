def solution(s):
    list_s = list(s)
    if list_s == s[::-1]:
        return len(list_s)

    result = list()
    for idx1, value1 in enumerate(list_s):
        idx2 = 0
        if value1 in list_s[idx1+1:]:
            for i, value2 in enumerate(list_s[idx1+1:]):
                if value2 in list_s[idx1+2:]:
                    if value1 == value2:
                        idx2 = idx1 + i + 2
                    if list_s[idx1:idx2] == list_s[idx1:idx2][::-1]:
                        result.append(len(list_s[idx1:idx2]))

    if len(result) == 0:
        return 1
    return max(result)

def solution(s):
    if s == s[::-1]:
        return len(s)

    result = []
    for i in range(len(s)):
        for j in range(0, i):
            chunk = s[j:i + 1]

            if chunk == chunk[::-1]:
                result.append(len(chunk))
    if len(result) == 0:
        return 1
    return max(result)


print(solution("abcdcbae"))
