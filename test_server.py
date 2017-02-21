from Fibonacci import FibonacciThreadedTCPRequestHandler, FibonacciThreadedTCPServer

'''
Module to test out the Fibonacci server
'''

address = ('localhost', 0)
server = FibonacciThreadedTCPServer(address)
print(server.server_address)
server.serve_forever()


