move_list = ["ход", "хода", "ходов"]
win_list = ["победа", "победы", "побед"]
lose_list = ["поражение", "поражения", "поражений"]

def bulls_and_cows(num1, num2):
    bc = [0, 0]
    for i in range(0, 4):
        if num2[i] in num1:
            if num2[i] == num1[i]:
                bc[0] += 1
            else:
                bc[1] += 1
    return bc

def try_number(num):
    if len(num) != 4 or not num.isdigit():
        return False
    for i in range(0, 3):
        for j in range(i + 1, 4):
            if num[i] == num[j]:
                return False
    return True

def endings(col):
    if col % 10 == 1 and col % 100 != 11:
        return 0
    if col % 10 in (2, 3, 4) and col % 100 not in (12, 13, 14):
        return 1
    return 2
