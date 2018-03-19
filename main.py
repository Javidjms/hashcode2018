import sys
import matplotlib.pyplot as plt


class Car(object):

    def __init__(self, id, r, c):
        self.id = id
        self.r = r  # Row
        self.c = c  # Column
        self.rides = []
        self.available_turn = 0

    def get_distance_to_ride(self, ride):
        return abs(self.r - ride.rb) + abs(self.c - ride.cb)

    def get_waiting_time(self, ride):
        distance = self.get_distance_to_ride(ride)
        return max(0, ride.tb - (distance + self.available_turn))

    def __repr__(self):
        return "Car {} - ({}, {})".format(self.id, self.r, self.c)


class Ride(object):

    def __init__(self, id, rb, cb, re, ce, tb, te, bonus):
        self.id = id
        self.rb = rb  # Row begin
        self.cb = cb  # Column begin
        self.re = re  # Row end
        self.ce = ce  # Column end
        self.tb = tb  # Earliest turn
        self.te = te  # Finished turn
        self.bonus = bonus
        self.car = None
        self.start_turn = None
        self.end_turn = None

    def get_bonus(self):
        if self.start_turn is None or self.start_turn > self.tb:
            return 0
        return self.bonus

    def get_distance(self):
        return abs(self.re - self.rb) + abs(self.ce - self.cb)

    def get_distance_to_next_ride(self, ride):
        return abs(self.re - ride.rb) + abs(self.ce - ride.cb)

    def get_score(self):
        if self.end_turn is None or self.end_turn >= self.te:
            return 0
        return self.get_distance() + self.get_bonus()

    def __repr__(self):
        return "Ride {} - ({}, {}) => ({}, {}) => ({}, {})".format(
            self.id, self.rb, self.cb, self.re, self.ce, self.tb, self.te
        )


class RMap(object):

    def __init__(self, rows, cols, nb_cars, nb_rides, bonus, turns, rides):
        self.rows = rows  # Max rows
        self.cols = cols  # Max cols
        self.nb_cars = nb_cars  # All cars
        self.nb_rides = nb_rides  # All rides
        self.bonus = bonus
        self.turns = turns  # Max turns

        self.cars = []
        for i in range(self.nb_cars):
            self.cars.append(Car(i, 0, 0))
        self.rides = rides


def init_nearest_ride(rides):
    for ride in rides:
        nearest_rides = sorted(rides, key=lambda r: ride.get_distance_to_next_ride(r))
        ride.next_ride = ride.get_distance_to_next_ride(nearest_rides[0])


def find_best_ride(turn, car, rides, max_turn):
    filter_func = lambda r: (
        r.car is None and
        turn < min(r.te, max_turn) and
        turn + car.get_distance_to_ride(r) + car.get_waiting_time(r) + r.get_distance() < min(r.te, max_turn)
    )
    sorted_func = lambda r: (
        # int((r.te - (turn + car.get_distance_to_ride(r) + car.get_waiting_time(r) + r.get_distance())) > 10),
        car.get_distance_to_ride(r) + car.get_waiting_time(r) + r.next_ride,
        -(r.get_distance() + (r.bonus if turn <= r.tb else 0)),
    )

    available_rides = filter(filter_func, rides)
    available_rides = sorted(available_rides, key=sorted_func)
    return available_rides[0] if len(available_rides) > 0 else None


def assign(turn, car, ride):
    complete_distance = car.get_distance_to_ride(ride) + ride.get_distance()

    ride.car = car
    ride.start_turn = turn + car.get_distance_to_ride(ride)
    ride.end_turn = turn + car.get_waiting_time(ride) + complete_distance

    car.r, car.c = ride.re, ride.ce
    car.available_turn = turn + car.get_waiting_time(ride) + complete_distance
    car.rides.append(ride)


def run(rmap):
    current_turn = 0
    init_nearest_ride(rmap.rides)
    while True:
        print("TURN", current_turn, rmap.turns)
        available_cars = filter(lambda c: current_turn >= c.available_turn, rmap.cars)

        for car in available_cars:
            ride = find_best_ride(current_turn, car, rmap.rides, rmap.turns)
            if ride is not None:
                assign(current_turn, car, ride)

        if current_turn == rmap.turns:
            break
        current_turn += 1


def read_file(filename):
    with open(filename, 'r') as f:
        first_line = [int(num) for num in f.readline().split()]
        max_rows, max_cols, nb_cars, nb_rides, bonus, steps = first_line

        rides = []
        for i in range(nb_rides):
            rb, cb, re, ce, tb, te = [int(num) for num in f.readline().split()]
            rides.append(Ride(i, rb, cb, re, ce, tb, te, bonus))
        rmap = RMap(max_rows, max_cols, nb_cars, nb_rides, bonus, steps, rides)
    return rmap


def write_file(rmap, filename):
    score = 0
    with open(filename, 'w') as f:
        for car in rmap.cars:
            f.write('{} '.format(len(car.rides)))
            for ride in car.rides:
                score += ride.get_score()
                f.write('{} '.format(ride.id))
            f.write('\n')
    print('SCORE : ', score)


def plot_rides(rides):
    for ride in rides:
        plt.plot([ride.rb * 5, ride.re * 5], [ride.cb * 5, ride.cb * 5], 'k-')
        plt.plot([ride.re * 5, ride.re * 5], [ride.cb * 5, ride.ce * 2], 'k-')
    plt.show()


def main():
    if len(sys.argv) < 3:
        sys.exit('Syntax: %s <filename> <output>' % sys.argv[0])

    print('Running on file: %s' % sys.argv[1])
    rmap = read_file(sys.argv[1])

    try:
        run(rmap)
    except KeyboardInterrupt:
        pass

    write_file(rmap, sys.argv[2])


if __name__ == '__main__':
    main()
