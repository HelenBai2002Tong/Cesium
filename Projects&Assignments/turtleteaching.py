import turtle as tt
tt.speed(0)
tt.fd(100)
tt.rt(90)
tt.penup()
tt.fd(200)
tt.pendown()
for i in range(50):
    tt.fd(50)
    tt.rt(100)

tt.bk(300)
tt.circle(30)
tt.clear()
tt.penup()
tt.home()
tt.setheading(90)
tt.pendown()
tt.hideturtle()
for i in range(100):
    tt.forward(100)
    tt.rt(90)

tt.mainloop()