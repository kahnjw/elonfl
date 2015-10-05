import sys

from run_season import run_season
from predict import predict


def main(args):

    if args[1] == 'runseason':
        if len(args) > 2:
            run_season(args[2])
        else:
            run_season()

    elif args[1] == 'predict' and len(args) >= 4:
        print(predict(float(args[2]), float(args[3])))

    else:
        raise Exception('Invalid number of args %s' % len(args))

if __name__ == '__main__':
    main(sys.argv)
