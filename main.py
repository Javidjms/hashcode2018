import sys


def read_file(filename):
    with open(filename, 'r') as f:
        first_line = [int(num) for num in f.readline().split()]
        max_rows, max_cols, nb_cars, nb_rides, bonus, steps = first_line

        rides = []
        for i in range(0, nb_rides):
            rb, cb, re, ce, tb, te = [int(num) for num in f.readline().split()]
            rides.append([rb, cb, re, ce, tb, te])
    return rides


def main():
    if len(sys.argv) < 2:
        sys.exit('Syntax: %s <filename>' % sys.argv[0])

    print('Running on file: %s' % sys.argv[1])
    rides = read_file(sys.argv[1])
    print(rides)




if __name__ == '__main__':
    main()
