from socketserver import ThreadingMixIn, TCPServer, BaseRequestHandler


class FibonacciThreadedTCPServer(ThreadingMixIn, TCPServer):
    """
    FibonacciThreadedTCPServer used to serve concurrent TCP requests for a fibonacci
    number. The server holds the lookup table fib_dict shared by each instance of
    FibonacciThreadedTCPRequestHandler to make optimized calculations.
    """

    def __init__(self, server_address, request_handler_class, bind_and_activate=True):
        TCPServer.__init__(self, server_address, request_handler_class, bind_and_activate=bind_and_activate)
        self.fib_dict = {0: 0, 1: 1, 2: 1}


class FibonacciThreadedTCPRequestHandler(BaseRequestHandler):
    """
    FibonacciThreadedTCPRequestHandler class for our server. One instance will be created to
    serve each request that comes into the server. Must override the handle() method which will
    be called by the server on each new instance for each incoming request
    """

    def handle(self):
        """
        reads in an integer from the incoming socket connection, calculates the fibonacci value of
        that number then returns that value to the socket

        :return: None
        """

        data = self.request.recv(1024).strip()
        print('Serving new request, data=%s' % data)
        try:
            num = int(data)
            if num < 0:
                raise ValueError
        except ValueError:
            self.request.sendall(bytes('Must send a valid number >= 0\n', 'ascii'))
            return

        # calculate the result of fib(num)
        result = self.calc_fib(self.server.fib_dict, num)
        # encode into bytes
        ret = bytes(str(result) + '\n', 'ascii')
        # return result
        self.request.sendall(ret)

    @staticmethod
    def calc_fib(fib_dict, n):
        """
        Calculates the fibonacci value of n in an optimized way using a lookup table
        and a linear calculation. Since the fib_table is a dictionary shared between
        multiple threads we can only write to the dict. Any type of read->modify->write
        sequence may be interrupted mid-execution, creating a race condition. If n is in
        the fib_dict we can simply return it, otherwise we can begin calculating each value
        of fib between the current highest value ( which is fib(len(fib_dict)-1) ) and n.

        :param fib_dict: the dictionary of fib numbers shared between threads
        :param n: the value of fib to calculate
        :return: fib(n)
        """
        if n not in fib_dict:
            length = len(fib_dict)
            while length <= n:
                fib_dict[length] = fib_dict[length - 1] + fib_dict[length - 2]
                length = len(fib_dict)
        return fib_dict[n]

# if module is imported this code won't run
if __name__ == '__main__':
    HOST, PORT = 'localhost', 0

    with FibonacciThreadedTCPServer((HOST, PORT), FibonacciThreadedTCPRequestHandler) as server:
        ip, port = server.server_address
        print("Starting FibServer at %s:%d" % (ip, port))
        print("Waiting for fibonacci requests...")
        server.serve_forever()
