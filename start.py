# Python program to illustrate the concept
# of threading
# importing the threading module
import os
import threading

def print_cube():
	"""
	function to print cube of given num
	"""
	os.system("python manage.py runserver")

def print_square():
	"""
	function to print square of given num
	"""
	os.system("python hello.py")

if __name__ == "__main__":
	# creating thread
	t1 = threading.Thread(target=print_square)
	t2 = threading.Thread(target=print_cube)

	# starting thread 1
	t1.start()
	# starting thread 2
	t2.start()

	# wait until thread 1 is completely executed
	t1.join()
	# wait until thread 2 is completely executed
	t2.join()

	# both threads completely executed
	print("Done!")
