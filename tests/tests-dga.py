

import inspect
import sys
import os

here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(here, "../src")))

from dga import *

def assertion(assertion, correct_msg, failure_msg):
	if assertion:
		print(correct_msg)
		return True
	else:
		print(failure_msg)
		return False

def test_strip_1():
	string = "helloworld.org.nz"
	stripped = strip_hld(string)
	ans = "helloworld"
	return assertion( stripped == ans,
		"Passed strip_1",
		"Failed strip_1: should be " + ans + " but it was " + stripped)

def test_strip_2():
	string = "helloworld.org.nz."
	stripped = strip_hld(string)
	ans = "helloworld"
	return assertion( stripped == ans,
		"Passed strip_2",
		"Failed strip_2: should be " + ans + " but it was " + stripped)

def test_strip_3():
	string = "hello.world.net.nz"
	stripped = strip_hld(string)
	ans = "hello.world"
	return assertion( stripped == ans,
		"Passed strip_3",
		"Failed strip_3: should be " + ans + " but it was " + stripped)

def test_strip_4():
	string = "hello.world.net.nz."
	stripped = strip_hld(string)
	ans = "hello.world"
	return assertion( stripped == ans,
		"Passed strip_4",
		"Failed strip_4: should be " + ans + " but it was " + stripped)

def test_strip_5():
	string = "hello.world.nz"
	stripped = strip_hld(string)
	ans = "hello.world"
	return assertion( stripped == ans,
		"Passed strip_5",
		"Failed strip_5: should be " + ans + " but it was " + stripped)

def test_strip_6():
	string = "hello.world.nz"
	stripped = strip_hld(string)
	ans = "hello.world"
	return assertion( stripped == ans,
		"Passed strip_6",
		"Failed strip_6: should be " + ans + " but it was " + stripped)

def test_strip_7():
	string = "johnny.nz"
	stripped = strip_hld(string)
	ans = "johnny"
	return assertion( stripped == ans,
		"Passed strip_7",
		"Failed strip_7: should be " + ans + " but it was " + stripped)

def test_strip_8():
	string = "johnny.nz."
	stripped = strip_hld(string)
	ans = "johnny"
	return assertion( stripped == ans,
		"Passed strip_8",
		"Failed strip_8: should be " + ans + " but it was " + stripped)

def main():

	tests = [obj for name,obj in inspect.getmembers(sys.modules[__name__]) if (inspect.isfunction(obj) and name.startswith("test"))]
	sortkey = lambda x : str(x)
	tests.sort(key=sortkey)
	print("=================")
	print(len(tests), "tests.")
	print("Running tests....")
	print()
	count = 0
	for test in tests:
		if test():
			count = count + 1
	pct = 1.0 * count / len(tests) * 100
	print()
	print("Finished.")
	print("Passed: " + str(count) + "/" + str(len(tests)) + " ("+str(pct)+"%)")
	print("================")
	
if __name__ == "__main__":
	main()