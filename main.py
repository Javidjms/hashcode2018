import sys


class Car(object):

    def __init__(self, id, r, c):
        self.id = id
        self.r = r
        self.c = c
        self.is_riding = False
        self.target = (-1, -1)

    def __repr__(self):
        return "Car {} - ({}, {})".format(self.id, self.r, self.c)


class Ride(object):

    def __init__(self, id, rb, cb, re, ce, tb, te):
        self.id = id
        self.rb = rb
        self.cb = cb
        self.re = re
        self.ce = ce
        self.tb = tb
        self.te = te
        self.is_done = False

    def __repr__(self):
        return "Ride {} - ({}, {}) => ({}, {}) => ({}, {})".format(
            self.id, self.rb, self.cb, self.re, self.ce, self.tb, self.te
        )


class RMap(object):

    def __init__(self, rows, cols, nb_cars, nb_rides, bonus, turns, rides):
        self.rows = rows
        self.cols = cols
        self.nb_cars = nb_cars
        self.nb_rides = nb_rides
        self.bonus = bonus
        self.turns = turns

        self.road_map = []
        for i in range(0, rows):
            self.road_map.append([0] * cols)

        self.cars = []
        for i in range(0, self.nb_cars):
            self.cars.append(Car(i, 0, 0))
        self.rides = rides
        # self.commands = []  # commands to put in output file


def read_file(filename):
    with open(filename, 'r') as f:
        first_line = [int(num) for num in f.readline().split()]
        max_rows, max_cols, nb_cars, nb_rides, bonus, steps = first_line

        rides = []
        for i in range(0, nb_rides):
            rb, cb, re, ce, tb, te = [int(num) for num in f.readline().split()]
            rides.append(Ride(i, rb, cb, re, ce, tb, te))
        rmap = RMap(max_rows, max_cols, nb_cars, nb_rides, bonus, steps, rides)
    return rmap


def assign(rmap):
    current_turn = 0

    while True:
        if current_turn == rmap.turns:
            break
        current_turn += 1


def main():
    if len(sys.argv) < 2:
        sys.exit('Syntax: %s <filename>' % sys.argv[0])

    print('Running on file: %s' % sys.argv[1])
    rmap = read_file(sys.argv[1])
    print(rmap.rides)

    assign(rmap)




if __name__ == '__main__':
    main()
