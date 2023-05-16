import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import random
from matplotlib.animation import FuncAnimation
from math import floor

class snake_game():
    moves = {0 : (0,1), 1 : (1,0), 2 : (0,-1), 3 : (-1,0)}
    snake_body = []
    curr_move = 1 # na poczatku idzie w prawo

    def __init__(self,a, b, n, s_length):
        self.fig = plt.figure()
        ax = self.fig.add_subplot(111)
        self.fig.suptitle('Snake is alive :)', fontsize=16, color='lime')
        plt.xlim([0, a])
        plt.ylim([0, b])
        plotlim = plt.xlim() + plt.ylim() 
        ax.imshow(([0,0],[1,1]) ,cmap=plt.cm.plasma, alpha=0.9, extent=plotlim, interpolation='bicubic')
        sqs = self.random_squares(a, b, n, s_length)
        snake_xy = [(round(a/2), i) for i in range(0,s_length)]
        for square in sqs:
            (x,y) = square
            r = Rectangle((x, y), 1, 1, facecolor ='black', edgecolor='red', linewidth=1.2)
            ax.add_patch(r)
        for i in range(0,s_length):
            r = Rectangle(snake_xy[i], 1, 1, facecolor ='cornflowerblue', edgecolor ='pink')
            ax.add_patch(r)
            self.snake_body.append(r)
        self.animation = FuncAnimation(self.fig, self.update, interval = 300, fargs=(snake_xy, s_length, a, b, sqs, ax))
        self.animation.running = True
        plt.show()

    def random_squares(self, a, b, n, s_length):
        if a % 2 == 0: # żeby nie wyjść poza wykres
            a -= 1
        if b % 2 == 0:
            b -= 1
        sqs = []
        for i in range(n):
            x = 2 * random.randint(0,floor(a/2))
            y = 2 * random.randint(0,floor(b/2))
            while (x,y) in sqs or (x >= round(a/2) - 1 and x <= round(a/2) + 1 and y <= s_length + 1):
                x = 2 * random.randint(0,floor(a/2)) # współrzędne kwadratów tylko parzyste - żeby żadne 2 kwadraty się nie stykały
                y = 2 * random.randint(0,floor(b/2))
            sqs.append((x,y))
        return sqs

    def random_move(self,curr_move, snake_xy, s_length, a, b, sqs):
        move = random.randint(0,3)
        while move % 2 == curr_move % 2 and move != curr_move: # jak idzie w prawo, to nie może zacząć iść w lewo itd.
            move = random.randint(0,3)
        (x,y) = snake_xy[s_length-1]
        (xm, ym) = self.moves[move]
        new_xy = ((x + xm) % a, (y + ym) % b)
        if new_xy in snake_xy:
            return self.random_move(curr_move, snake_xy, s_length, a, b, sqs) # żeby nie wchodził drugi raz na pole, które zajmuje jego inna część
        for i in range(s_length - 1):
            snake_xy[i] = snake_xy[i + 1]
        snake_xy[s_length - 1] = new_xy
        if new_xy in sqs:
            curr_move = -1
        else:
            curr_move = move
        return curr_move
    
    def update(self,i, snake_xy, s_length, a, b, sqs, ax):
        self.curr_move = self.random_move(self.curr_move, snake_xy, s_length, a, b, sqs)
        if self.curr_move == -1:
            self.snake_body[0].remove()
            r = Rectangle(snake_xy[s_length-1], 1, 1, facecolor ='cornflowerblue', edgecolor ='red', linewidth=2)
            ax.add_patch(r)
            self.fig.suptitle('Snake is dead :(', fontsize=16, color='crimson')
            self.animation.event_source.stop()
        else:
            self.snake_body[0].remove()
            self.snake_body.remove(self.snake_body[0])
            r = Rectangle(snake_xy[s_length-1], 1, 1, facecolor ='cornflowerblue', edgecolor ='pink')
            ax.add_patch(r)
            self.snake_body.append(r)

snake_game(20, 20, 16, 6)


