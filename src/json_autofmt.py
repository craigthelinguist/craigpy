
import json, argparse

def main():
	parser = argparse.ArgumentParser('Auto format a .json file')
	parser.add_argument('--input', required=True, help='file to autofmt')
	parser.add_argument('--out', required=True, help='where to output formatted file')
	json_struct = None
	with open(parser.input, 'rb') as f:
		json_struct = json.load(f)
	with open(parser.out, 'wb') as f:
		json.dump(json_struct, f, indent=2)

if __name__ == '__main__':
	main()
