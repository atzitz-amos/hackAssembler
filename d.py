_regex = "abc[a-z]+[0-9]{2}"


def parse(regex: str) -> list:
    nodes = []
    i = 0
    while i < len(regex):
        match regex[i]:
            case "[":
                j = i
                while j < len(regex) and regex[j] != "]":
                    j += 1
                nodes.append(parse(regex[i + 1:j]))
                i = j
            case "-":
                last = nodes.pop()
                nodes.append((last[0], ord(regex[i + 1])))
                i += 1
            case "+" | "*":
                nodes.append((*nodes.pop(), regex[i]))
            case "{":
                j = i
                while j < len(regex) and regex[j] != "}":
                    j += 1
                nodes.append((*nodes.pop(), int(regex[i + 1:j])))
                i = j
            case _:
                nodes.append((ord(regex[i]),))
        i += 1

    return nodes


def match(s, regex):
    i = 0
    for node in regex:
        match node:
            case ((c1, c2), ):
                if i < len(s) and c1 <= ord(s[i]) <= c2:
                    i += 1
                else:
                    return False
            case ((c1, c2), "+"):
                while i < len(s) and c1 <= ord(s[i]) <= c2:
                    i += 1
                else:
                    return False
            case ((c1, c2), "*"):
                while i < len(s) and c1 <= ord(s[i]) <= c2:
                    i += 1
            case ((c1, c2), n):
                for _ in range(n):
                    if i < len(s) and c1 <= ord(s[i]) <= c2:
                        i += 1
                    else:
                        return False
            case (c, ):
                if i < len(s) and s[i] == chr(c):
                    i += 1
                else:
                    return False
            case (c, "+"):
                while i < len(s) and s[i] == chr(c):
                    i += 1
                else:
                    return False
            case (c, "*"):
                while i < len(s) and s[i] == chr(c):
                    i += 1
            case (c, n):
                for _ in range(n):
                    if i < len(s) and s[i] == chr(c):
                        i += 1
                    else:
                        return False
            case (c1, c2):
                if i < len(s) and c1 <= ord(s[i]) <= c2:
                    i += 1
                else:
                    return False
    return True


print(match("abc", parse("abc[a-z]{2}")))


# ---------------
def findAll(string, value):
    i = j = 0
    result = []
    if not value:
        return result
    while i < len(string):
        if j == len(value):
            j = 0
            result.append((i - len(value), i))
        if string[i] == value[j]:
            j += 1
        i += 1
    if j == len(value):
        result.append((i - len(value), i))
    return result


print(findAll("adbbc1bc23bc", "bc"))
