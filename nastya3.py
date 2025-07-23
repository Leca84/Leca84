'''a= int(input())
b= int(input())
if a<=b:
    print(a)
if b<a:
    print(b)
a= int(input())
if a > 0:
    print(1)
elif a < 0:
    print(-1)
else:
    print(0)'''
#шахматная доска
x1 = int(input())
y1 = int(input())
x2 = int(input())
y2 = int(input())
if (x1 + y1) % 2 == (x2 + y2) % 2:
    print("YES")
else:
    print("NO")