import random as rd
import pygame as pg
import sys
def share_diagonal(x0, y0, x1, y1):
    """ Is (x0, y0) on a shared diagonal with (x1, y1)? """
    dy = abs(y1 - y0)        # Calc the absolute y distance
    dx = abs(x1 - x0)        # CXalc the absolute x distance
    return dx == dy          # They clash if dx == dy
def col_clashes(bs, c):
    """ Return True if the queen at column c clashes
         with any queen to its left.
    """
    for i in range(c):     # Look at all columns to the left of c
          if share_diagonal(i, bs[i], c, bs[c]):
              return True

    return False
def has_clashes(the_board):
    """ Determine whether we have any queens clashing on the diagonals.
        We're assuming here that the_board is a permutation of column
        numbers, so we're not explicitly checking row or column clashes.
    """
    for col in range(1,len(the_board)):
        if col_clashes(the_board, col):
            return True
    return False

def has_clash(list):
    k=0
    for i in range(len(list)):
        if i == list[i] or i ==list[-i-1]:
            k=k+1
    if k > 1:
        return True
    else:
        return False

def main():
    k=eval(input("numbers you want the chessboard to be:"))
    list=[]
    for i in range(k):
        list.append(i)
    found=0
    if k > 2:
        q=eval(input("numbers of solution you want:"))
        while found<q:
            rd.shuffle(list)
            if not has_clashes(list):
                draw_board(list,k)
                found=found+1
    else:
        draw_board(list,k)
def draw_board(list,f):
    pg.init()
    screencaption = pg.display.set_caption('eight_queen')
    colors=[(255,0,0),(0,0,0)]
    num=len(list)
    screensize=480
    each=screensize//num
    screensize=each*num
    screen=pg.display.set_mode((screensize,screensize))

    crown=pg.image.load("crown.png")
    crown=pg.transform.scale(crown, (each, each))
    crown_offset=(each-crown.get_width())//2

    error=pg.image.load("error.png")
    error=pg.transform.scale(error,(screensize,screensize))
    if f < 3 :
        while True:
            ev = pg.event.poll()

            if ev.type == pg.QUIT:
                sys.exit()
            screen.blit(error,(0,0))

            pg.display.flip()
    else:
        while True:
            ev = pg.event.poll()
            if ev.type == pg.KEYDOWN:
                if ev.key == pg.K_SPACE:
                    break
            if ev.type == pg.QUIT:
                sys.exit()

            for i in range(num) :
                k=i%2
                for j in range(num):
                    pg.draw.rect(screen,colors[k], [i*each,j*each, each, each], 0)
                    if k ==0:
                        k=k+1
                    else:
                        k=k-1

           # for i in range(len(list)):
                #screen.blit(crown,i*each+crown_offset,list[i]*each+crown_offset)
            for (col, row) in enumerate(list):
                screen.blit(crown,
                             (col * each + crown_offset, row * each + crown_offset))

            pg.display.flip()
        pg.quit()
main()
