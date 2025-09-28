'''import turtle
t=turtle.Pen()
for x in range(4):
    t.circle(100)
    t.left(90)
import turtle
t=turtle.Pen()
for x in range(6):
    t.circle(100)
    t.left(60)
import turtle
t=turtle.Pen()
number_of_circles=int(turtle.numinput("количество окружностей","сколько окружностей в вашей розетке?", 6))
for x in range(number_of_circles):
    turtle.speed(10)
    t.circle(100)
    t.left(360/number_of_circles)
name=input("как тебя зовут?")
while name != " ":
    for x in range(100):
        print(name, end = " ")
    print()
    name=input("введите еще имя или нажмите [Enter], чтобы выйти: ")
print("💩💩💩💩💩💩💩")
import turtle
t=turtle.Pen()
turtle.bgcolor("black")
colors = ["red", "yellow", "blue", "green", "orange", "purple", "white", "brown", "gray", "pink"]
family = turtle.textinput("моя семья", "введите имя или нажмите [enter], чтобы выйти:")
while name != "":
    family.append(name)
    name = turtle.textinput("моя семья", "введите имя или нажмите [Enter], чтобы выйти: ")
for x in range(100):
    t.pencolor(colors[x%len(family)])
    t.penup()
    t.forward(x*4)
    t.pendow()
    t.white(family[x%len(family)], font = ("Arial", int((x+4)/4), "bold"))
    t.left(360/len(family)+2)
import turtle
t=turtle.Pen()
t.penup()
turtle.bgcolor("black")
sides=int(turtle.numinput("количество стороне у вашей спирали (2-6)?", 4, 2, 6))
colors = ["red", "yellow", "blue", "green", "orange", "purple"]
for m in range(100):
    t.forward(m*4)
    position = t.position()
    heading = t.heading()
    for n in range (int(m/2)):
        t.pendown()
        t.pencolor(colors[n%siders])
        t.forward(2*n)
        t.right(360/sides - 2)
        t.penup()
    t.setx(position[0])
    t.sety(position[1])
    t.setheading(heading)
    t.left(360/len(family)+2)'''
for i in range(4):
    sl=input
    print(sl+sl)