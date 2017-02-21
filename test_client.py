from Fibonacci import HumanClient, AutoClient

'''
Module to test out the Fibonacci client
'''

ip = 'localhost'
port = int(input('Please enter the port number of the Fibonacci server: '))

test_auto = True

if test_auto:
    client = AutoClient(ip, port)
    client.connect(num_threads=50, fib_min=4000, fib_max=5000, verbose=False, silent=False)
else:
    client = HumanClient(ip, port)
    client.connect()

