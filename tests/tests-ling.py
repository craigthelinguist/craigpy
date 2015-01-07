import strmetric
import inspect
import sys

def assertion(assertion, correct_msg, failure_msg):
	if assertion:
		print(correct_msg)
		return True
	else:
		print(failure_msg)
		return False

def test_seq_score_1():
	s1 = "john"
	s2 = "ohm"
	ans = strmetric.seq_align(s1, s2)
	correct_ans = -1
	return assertion(ans==correct_ans,
		"Passed seq_score_1",
		"Failed seq_score_1: got " + str(ans) + " but should have been " + str(correct_ans))

def test_seq_score_2():
	s1 = "john"
	ans = strmetric.seq_align(s1, s1)
	return assertion(ans==4,
		"Passed seq_score_2",
		"Failed seq_score_2: got " + str(ans) + " but should have been 4")

def test_seq_score_3():
	s1 = "john"
	ans = strmetric.seq_align(s1, s1)
	return assertion(ans==4,
		"Passed seq_score_3",
		"Failed seq_score_3: got " + str(ans) + " but should have been 4")

def test_seq_score_4():
	s1 = "john"
	s2=  "John"
	ans = strmetric.seq_align(s1, s2, case_sensitive=True)
	return assertion(ans==2,
		"Passed seq_score_4",
		"Failed seq_score_4: got " + str(ans) + " but should have been 2")

def test_seq_score_5():
	s1 = "john"
	s2 = "ohm"
	ans = strmetric.seq_align(s1, s2, match=4, mismatch=-5, skip=-10)
	correct_ans = -7
	return assertion(ans==correct_ans,
		"Passed seq_score_5",
		"Failed seq_score_5: got " + str(ans) + " but should have been " + str(correct_ans))

def test_seq_score_6():
	s1 = "john"
	s2 = "JoHn"
	ans = strmetric.seq_align(s1, s2, match=2, mismatch=-3, skip=-5, case_sensitive=True)
	correct_ans = - 3 + 2 - 3 + 2
	return assertion(ans==correct_ans,
		"Passed seq_score_6",
		"Failed seq_score_6: got "+ str(ans) +" but should have been " + str(correct_ans))

def test_seq_align_1():
	s1 = "john"
	s2 = "ohm"
	align = strmetric.alignment(s1, s2)
	correct_ans = ("john","_ohm")
	return assertion(align == correct_ans,
		"Passed seq_align_1",
		"Failed seq_align_1: got " + str(align) + " but should have been " + str(correct_ans))

def test_seq_align_2():
	s1 = "john"
	s2 = "ohm"
	align = strmetric.alignment(s1, s2, pad_character="&")
	correct_ans = ("john", "&ohm")
	return assertion(align == correct_ans,
		"Passed seq_align_2",
		"Failed seq_align_1: got " + str(align) + " but should have been " + str(correct_ans))

 
def main():
	print("=================")
	print("Running tests....")
	print()
	tests = [obj for name,obj in inspect.getmembers(sys.modules[__name__]) if (inspect.isfunction(obj) and name.startswith("test"))]
	sortkey = lambda x : str(x)
	tests.sort(key=sortkey)
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