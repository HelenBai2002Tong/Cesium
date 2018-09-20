import turtle

turtle.speed(7)
turtle.hideturtle()
turtle.bgcolor("lavenderblush")
def draw_branch(branch_length):
    if branch_length > 5:
        if branch_length < 40:
            turtle.color('palevioletred')
        else:
            turtle.color('pink')
        turtle.forward(branch_length)
        turtle.right(25)
        draw_branch(branch_length-15)
        turtle.left(50)
        draw_branch(branch_length-15)
        if branch_length < 40:
            turtle.color('palevioletred')
        else:
            turtle.color('pink')
        turtle.right(25)
        turtle.backward(branch_length)

turtle.color('palevioletred')
turtle.right(90)
turtle.fd(100)
turtle.left(180)
draw_branch(100)
