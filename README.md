# FibbonacciServer
A class assignment to create a multithreaded fibonacci server/client

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

Using Python, design a socket server that will accept an integer and return a fibonacci value for the integer. Design a
reliable protocol and implement both a client and server for calculating our Fibonacci values. Ensure that you can have more than one calculation occurring at any moment.
'''

The server is optimized (hah! python threads) to serve many concurrent requests for very large fibonacci values up to around fib(100000). 

