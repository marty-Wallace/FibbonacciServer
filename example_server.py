from Fibonacci import FibonacciThreadedTCPServer

'''
Example file showing how to use the Fibonacci server
'''

address = ('localhost', 0)
server = FibonacciThreadedTCPServer(address)
print(server.server_address)
server.serve_forever()


