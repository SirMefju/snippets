import argparse


#inicialize
parser = argparse.ArgumentParser(description='Description for -h flag')
# flag, name, type, alignment, requirement, help description
parser.add_argument('-w', '--welcome', type=str, metavar='', required=True, help='description')
# reference
args = parser.parse_args()


def function(argument):
    print(Hello world!)
    
def main():
    function(args.welcome)

if __name__ == '__main__':
    main()