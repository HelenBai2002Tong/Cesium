def reversefile(a):
    """
    :param a: a string of the file name(.txt)
    :return: a file(txt) which is in reverse order of the file a
    """
    f = open(a, "r")
    xs = f.readlines()
    f.close()
    g = open("reverse.txt", "w")
    for i in range(len(xs)-1,-1,-1):
        g.write(xs[i])
    g.close()

def print_only_snake(a):
    """
    :param a: a string of the file name(.txt)
    :return: prints the lines that contain the substring snake.
    """
    f = open(a, "r")
    xs = f.readlines()
    f.close()
    for v in xs:
        if "snake" in v:
            print(v,end="")

def add_number(a):
    """

    :param a: a string of the file name(.txt)
    :return: produces an output file which is a copy of the file, except the first five columns of each
    line contain a four digit line number, followed by a space.
    """
    f = open(a,"r")
    xs=f.readlines()
    f.close()
    q = open("add_number.txt","w")
    num=1
    for v in xs:
        v="%04d"%num+' '+v
        num+=1
        q.write(v)
    q.close()


def delete_number(a):
    """
    :param a:a string of the file name(.txt)
    :return: a file delete the serial number of it
    """
    f = open(a,"r")
    xs=f.readlines()
    f.close()
    q = open("delete_number.txt", "w")
    for v in xs:
        v=v[5:]
        q.write(v)
    q.close()