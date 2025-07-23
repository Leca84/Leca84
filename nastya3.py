#задача на минимум
#правильно
a = int(input())
b = int(input())
if a<=b:
    print(a)
if b<a:
    print(b)
#знак числа
#правильно
a= int(input())
if a > 0:
    print(1)
elif a < 0:
    print(-1)
else:
    print(0)
#шахматная доска
#правильно
x1 = int(input())
y1 = int(input())
x2 = int(input())
y2 = int(input())
if (x1 + y1) % 2 == (x2 + y2) % 2:
    print("YES")
else:
    print("NO")
#високостный год
#неправильно, исправил. сначала проверяем делится ли на 400, если не делится то делится ли на 100, 
#если не делится то делится ли на 4, и если нет то значит не високосный
a = int(input())
#if (a % 400 == 0) or (a % 4 == 0):
if (a % 400 == 0):
    print("YES")
else:
    if (a % 100 == 0):
        print("NO")
    else:
        if (a % 4 == 0):
            print("YES")
        else:
            print("NO")
      
