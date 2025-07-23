# минимум из двух чисел
a = int(input())
b = int(input())
if a < b:
    print(a)
else:
    print(b)



# знак числа
x = int(input())
if x > 0:
    print(1)
elif x < 0:
    print(-1)
else:
    print(0)


# шахматная доска
x1, y1 = int(input()), int(input()) 
x2, y2 = int(input()), int(input()) 
if (x1 + y1) % 2 == (x2 + y2) % 2:
    print("YES")
else:
    print("NO")        


# Високостный год
    year = int(input())
if (year % 4 = 0 and year % 100 != 0) or (year% 400 ==0):
    print("YES")
else:
    print("NO")



# минимум из трёх чисел
a = int(input())
b = int(input())
c = int(input())
if a <= b and a <= c:
    print(a)
elif b <= a and b <= c:
    print(b)
else:
    print(c)


# сколько чисел совподает
a = int(input())
b = int(input())
c = int(input())
if a == b == c:
    print(3)
elif a == b or a == c or b = c:
    print(2)
else:
    print(0)

# ход ладьи
x1 = int(input())
y1 = int(input())
x2 = int(input())
y2 = int(input())
if x1 == x2 or y1 == y2:
    print("YES")
else:
    print(NO)

# ход короля
x1 = int(input())
y1 = int(input())
x2 = int(input())
y2 = int(input())
if abs(x1 - x2) <= 1 and abs(y1 - y2) <= 1:
    print("YES")
else
    print("NO")



# ход слона
x1 = int(input()
y1 = int(input())
x2 = int(input())
y2 = int(input())
if abs(x1 - x2) = abs(y1 - y2):
    print("YES")
else:
    print("NO")


# ход ферзя
x1 = int(input())
y1 = int(input())
x2 = int(input())
y2 = int(input())
if (x1 == x2) or (y1 == y2) or (abs(x1 - x2) = abs(y1 - y2)):
    print("YES")
else:
    print("NO")




# ход коня
x1 = int(input())
x2 = int(input())
y1 = int(input())
y2 = int(input())
if x1 == x2 or y1 == y2 or abs(x1 - x2) == abs(y1 - y2):
    print("YES")
else:
    print("NO")
