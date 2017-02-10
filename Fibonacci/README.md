
My implementation of a school assignment with the following requirements

'''
Given that our Fibonacci calculation looks like:
def fib(n):
   if n == 0:
       return 0
   elif n == 1:
       return 1
   else:
       return fib(n-1) + fib(n-2)
Using Python, design a socket server that will accept an unsigned integer (properly packed) and return a fibonacci value for the integer. Design a
reliable protocol and implement both a client and server for calculating our Fibonacci values. Ensure that you can have more than one calculation
occurring at any moment.
'''

###fib_server
fib_server.py contains two classes FibonacciThreadedTCPRequestHandler and FibonacciThreadedTCPServer. Which can be implemented by following the example in test_client.py. I have optimized the calculations of the fibonacci numbers as far as I can and on my Dell Inspirion I am able to have 50 threads requesting fib numbers up to fib(50000) concurrently without any timeouts or incorrect answers.

###fib_client
fib_client.py also contains two classes as well as command line main function which accepts several args and options for it's auto tester function. An example of how to use the two fib_client classes is available in test_client.py. The two classes are HumanClient and AutoClient. HumanClient runs a loop forever requesting a number from the user then requesting the fib value of that number from the server. AutoClient accepts several parameters such as the number of threads/concurrent requests to use, the minimum and maximum fib values to request and the level of verbosity it should use when printing out (printing all the numbers when requesting 100 fib(50000)'s will fill up your terminal very quickly).

To view the command line opts and args for the auto tester simply run python FibClient.py --help.

To run an instance of the server from the command line simply run python FibServer.py. It will request a port number from the kernel automatically.