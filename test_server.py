from Fibonacci import FibonacciThreadedTCPRequestHandler, FibonacciThreadedTCPServer

'''
Module to test out the Fibonacci server
'''
server = FibonacciThreadedTCPServer(('localhost', 0), FibonacciThreadedTCPRequestHandler)
print(server.server_address)
server.serve_forever()


