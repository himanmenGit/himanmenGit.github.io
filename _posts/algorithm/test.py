def solution(s):
    if s.count('(') == s.count(')') and s[0] == '(' and s[-1] == ')':
        count = 0
        for v in s:
            if v == '(':
                count += 1
            else:
                if count > 0:
                    count -= 1
                else:
                    return False
        return True
    return False


print(solution('()()'))
print(solution(')()('))
print(solution('())(()'))
