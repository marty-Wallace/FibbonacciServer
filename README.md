# FibbonacciServer
A class assignment to create a multithreaded fibonacci server/client

My implementation of a school assignment with the following requirements

Given that our Fibonacci calculation looks like:
```
def fib(n):
   if n == 0:
       return 0
   elif n == 1:
       return 1
   else:
       return fib(n-1) + fib(n-2)
```

Using Python, design a socket server that will accept an integer and return a fibonacci value for the integer. Design a
reliable protocol and implement both a client and server for calculating our Fibonacci values. Ensure that you can have more than one calculation occurring at any moment.


The server is set up to serve many concurrent Fibonacci requests for very large values up to around fib(100000). The server uses a lookup table that is shared among each thread. All fibonacci numbers are calculated using a linear definition rather than a recursive one and each value is stored in the cache table. To keep the dictionary "safe" the data is written to the dictionary in the form of:
```
def calc_fib(fib_dict, n):
     length = len(fib_dict)
     while length <= n:
         fib_dict[length] = fib_dict[length - 1] + fib_dict[length - 2]
         length = len(fib_dict)
return fib_dict[n]
```
In this format it is possible for many threads to write to the same location in the dictionary but since each number is based on the previous two numbers the data will stay intact. The length is updated to the length of the actual dict at the end of each loop iteration to avoid doing work done in other threads (as opposed to length += 1). 

