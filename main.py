import sys


def compute_distance(car, ride):
    distance1 = abs(ride.rb - car.r) + abs(ride.cb - car.c)
    distance2 = abs(ride.rb - ride.re) + abs(ride.cb - ride.ce)
    return distance1 + distance2


class Car(object):

    def __init__(self, id, r, c):
        self.id = id
        self.r = r
        self.c = c
        self.is_active = False
        self.has_prepared_ride = False
        self.target = (-1, -1)
        self.rides = []

    def check_target_reached(self):
        return self.target == (self.r, self.c)

    def move(self):
        if self.r != self.target[0]:
            direction = 1 if self.target[0] - self.r > 0 else -1
            self.r += direction
        elif self.c != self.target[1]:
            direction = 1 if self.target[1] - self.c > 0 else -1
            self.c += direction
        else:
            pass

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
        self.car = None

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

        self.cars = []
        for i in range(1, self.nb_cars + 1):
            self.cars.append(Car(i, 0, 0))
        self.rides = rides


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


def find_best_ride(car, rides):
    # func = lambda r: compute_distance(car, r)
    rides.sort(key=lambda r: (r.tb, compute_distance(car, r)))
    return rides[0] if len(rides) else None


def run(rmap):
    current_turn = 0
    while True:
        print(current_turn, rmap.turns)
        available_rides = list(filter(lambda c: not c.car, rmap.rides))
        available_cars = list(filter(lambda c: not c.is_active, rmap.cars))

        # Assign ride to free cars
        for car in available_cars:
            ride = find_best_ride(car, available_rides)
            # ride = available_rides[0] if len(available_rides) else None
            if ride:
                ride.car = car
                car.rides.append(ride)
                car.target = (ride.rb, ride.cb)
                car.is_active = True
                available_rides.remove(ride)

        active_cars = list(filter(lambda c: c.is_active, rmap.cars))

        for car in active_cars:
            current_ride = car.rides[-1]
            if car.is_active and not car.has_prepared_ride and car.check_target_reached():
                car.has_prepared_ride = True
                car.target = (current_ride.re, current_ride.ce)

            if (car.is_active and not car.has_prepared_ride) or \
               (car.is_active and car.has_prepared_ride and
               current_turn >= current_ride.tb):
                car.move()

            if car.is_active and car.has_prepared_ride and car.check_target_reached():
                car.has_prepared_ride = False
                car.is_active = False

        if current_turn == rmap.turns:
            break
        current_turn += 1


def write_file(rmap, filename):
    with open(filename, 'w') as f:
        for car in rmap.cars:
            f.write(' '.join(
                [str(car.id)] + [str(ride.id) for ride in car.rides]) + '\n'
            )


def main():
    if len(sys.argv) < 3:
        sys.exit('Syntax: %s <filename> <output>' % sys.argv[0])

    print('Running on file: %s' % sys.argv[1])
    rmap = read_file(sys.argv[1])
    # print(rmap.rides)

    run(rmap)

    write_file(rmap, sys.argv[2])


if __name__ == '__main__':
    main()
