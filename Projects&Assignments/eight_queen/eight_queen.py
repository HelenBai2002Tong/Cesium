import random as rd
import pygame as pg
import sys
def has_clashes(list):
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
    if f < 3:
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
