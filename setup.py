import argparse

parser = argparse.ArgumentParser(description='A setup script to process metadata based on the version')
parser.add_argument('--version', '-v', default='v1', help='Specify the version (default: v1)')
args = parser.parse_args()

if args.version == 'v1':
    from convert.v1 import convert_all
    convert_all()
else:
    from convert.v1 import convert_all
    print('This is only supported version v1')
    convert_all()
print(f'Converted version: {args.version}')