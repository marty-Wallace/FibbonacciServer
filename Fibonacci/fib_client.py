import socket
import sys
import getopt

from threading import Thread
from random import randint


class FibClient(object):
    """
    Base Class for the AutoClient and HumanClient to extend from. Implements some of the shared methods/attributes
    """
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    @staticmethod
    def receive_from_sock(sock, buffer_size):
        """
        Generator function to yield the current buffer received from sock.
        Can be used in the form of b''.join(recv_all(sock, buffer_size)) to
        receive the full transmission from a socket

        :param sock: the socket to receive data from
        :param buffer_size: the size of the buffer to load on each yield
        :return: yields the current buffer as a byte object
        """
        message_buffer = sock.recv(buffer_size)
        while message_buffer:
            yield message_buffer
            message_buffer = sock.recv(buffer_size)

    @staticmethod
    def receive_all_from_sock(sock, buffer_size=2048):
        """
        Builds the full message received from a socket in bytes

        :param sock: the socket to receive data from
        :param buffer_size: the size of the buffer to load while building full result, defaults to 2048
        :return: byte object containing full message
        """
        return b''.join(FibClient.receive_from_sock(sock, buffer_size))

    def get_fibonacci_number(self, number):
        """
        Make a request to the fib server for a single fib number. If there is a socket or value error, return None

        :param number: the fib number to request from the server
        :return: fib of n, if an error occurs then None
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.ip, self.port))
        response = None
        try:
            sock.sendall(bytes(str(number), 'ascii'))
            response = int(FibClient.receive_all_from_sock(sock))
        except socket.error as err:
            print(err, file=sys.stderr)
        except ValueError as err:
            print(err, file=sys.stderr)
        finally:
            sock.close()
            return response


class AutoClient(FibClient):
    """
    Class to do automated testing on the fibonacci server. Capable of spinning up multiple threads
    and requesting random fib numbers then testing their correctness.
    """

    def _test_fib(self, number, verbose, silent):
        """
        Requests a single fib number from the server then does the calculation locally to
        ensure that the number is correct

        :param number: the fib number to request/test
        :param verbose flag if the printing level is high
        :param silent flag if the printing level is for errors only
        :return: None
        """

        def local_fib(n):
            """
            Generate the fib number locally to test against the server's result
            :param n: the fib number to generate
            :return: fib of n
            """
            a, b = 1, 1
            for i in range(n-1):
                a, b = b, a+b
            return a

        # get server result
        result = self.get_fibonacci_number(number)
        # server errors will return None so check for None
        if result is None:
            if verbose:
                print('Received None from server')
            return None

        if not silent:
            print('Received result %d from server for fib(%d)' % (result, number))

        # get local result
        local_result = local_fib(number)
        if verbose:
            print('Calculated local value to be %d for fib(%d)' % (local_result, number))

        # compare results
        if result != local_result:
            # even on silent we will display errors of this kind.
            # if we enter this block it means the server is returning wrong numbers
            print("Server returned %d for fib(%d) should have been %d" % (result, number, local_result))

    def connect(self, num_threads=15, fib_min=1, fib_max=2000, verbose=False, silent=False):
        """
        Runs some automated tests on the server by spinning up multiple concurrent clients, one to a thread,
        each requesting a random fib number and double checking the results returned by the server

        :param num_threads: the number of threads/clients to spin up concurrently. Defaults to 15
        :param fib_min: the minimum fib number to request from the server. Defaults to 1
        :param fib_max: the maximum fib number to request from the server. Defaults to 2000
        :param verbose: sets the highest level of printing out whats going on
        :param silent: sets the lowest level of printing out whats going on
        :return: None
        """
        threads = []

        for i in range(num_threads):
            num = randint(fib_min, fib_max)
            if verbose:
                print('Starting thread with target number %d' % num)
            threads.append(Thread(target=self._test_fib, args=(num, verbose, silent)))

        for thread in threads:
            thread.start()


class HumanClient(FibClient):

    def __init__(self, ip, port):
        super().__init__(ip, port)

    def connect(self):
        """
         A loop that allows a human to repeatedly request fib numbers from the server.

        :return: None
        """
        while True:
            bad_input = True
            num = 0
            while bad_input:
                try:
                    num = int(input('Please enter which fibonacci number you would like: '))
                    if num <= 0:
                        print("Please enter a positive number. Negative fibonacci numbers are undefined.")
                    else:
                        bad_input = False
                except ValueError as err:
                    print("Please enter a number")
                    continue
            fib = self.get_fibonacci_number(num)
            if fib is None:
                print('Error: None returned by get_fibonacci_number(%s, %d, %d)' % (ip, port, num))
                continue
            print("Fib of %d is %d" % (num, fib))
            print() # blank line


def usage(message=''):
    """
    Displays a set of messages describing how to use the program
    :param message: an optional message to display at the beggining of the output
    :return: None
    """
    if message != '':
        print(message)

    print('fib_client.py improper usage')
    print('Usage: python fib_client.py --port=<portnumber> [options] ')
    print('Options are:')
    print('  -i, --ip=        ip address of the fib server, defaults to localhost')
    print('  -p, --port=      port address of the server, required argument')
    print('  -a, --auto       sets that we are going to use the auto tester client rather than the human client')
    print('  -t, --threads=   only applies to the auto tester and it sets how many concurrent requests to make')
    print('  -l, --low=       sets the lowest fib number to randomly request for the auto client defaults to 1')
    print('  -h, --high=      sets the highest fib number to randomly request for the auto client defaults to 2000')
    print('  -s, --silent     sets the output level to silent for auto-testing (useful for large numbers)')
    print('  -v, --verbose    sets output level to verbose for auto-testing')
    print('  --help           requests this usage screen')
    exit()


def main():
    """
    Reads in opts and args from the command line and then takes the appropriate action
    to either start up the human client or the auto-tester client.
    """

    ip = '127.0.0.1'  # ip address of the server
    port = -1         # port of the server must be set by args
    auto = False      # flag to run auto_client over human_client
    threads = 15      # number of threads to run auto_client with
    low = 1           # lowest fib number to request with auto_client
    high = 2000       # highest fib number to request with auto_client
    silent = False    # print nothing during auto_testing
    verbose = False   # print everything during auto-testing

    # reads in all opts and args and sets appropriate variables
    try:
        opts, args = getopt.getopt(sys.argv[1:], "i:p:at:l:h:sv",
                                   ["ip=", "port=", "auto", "threads=", "low=", "high=", "silent", "verbose"])
    except getopt.GetoptError:
        usage()
    for o, a in opts:
        # ip address
        if o in ('-i', '--ip'):
            ip = a
        # port number
        elif o in ('-p', '--port'):
            try:
                port = int(a)
            except ValueError:
                usage("Port must be a number")
        # auto client
        elif o in ('-a', '--auto'):
            auto = True
        # threads
        elif o in ('-t', '--threads'):
            try:
                threads = int(a)
            except ValueError:
                usage("Number of threads must be a number")
        # low value
        elif o in ('-l', '--low'):
            try:
                low = int(a)
                if low < 1:
                    raise ValueError
            except ValueError:
                usage("Low must be a number greater than 0")
        # high value
        elif o in ('-h', '--high'):
            try:
                high = int(a)
                if high < 1:
                    raise ValueError
            except ValueError:
                usage("High must be a number greater than 0")
        # verbose
        elif o in ('-v', '--verbose'):
            if silent:
                usage('Cannot set both verbose and silent to be true')
            verbose = True
        # silent
        elif o in ('-s', '--silent'):
            if verbose:
                usage('Cannot set both verbose and silent to be true')
            silent = True
        # any other args/opts show usage
        else:
            usage()

    # ensure port is set
    if port == -1:
        usage('The port number must be set')

    # make sure our numbers make sense, take low if they don't
    if high < low:
        high = low

    if auto:
        if verbose:
            print('Target server at %s:%d' % (ip, port))
            print('Starting %d threads requesting numbers between %d-%d' % (threads, low, high))

        AutoClient(ip, port).connect(num_threads=threads, fib_min=low, fib_max=high, verbose=verbose, silent=silent)
    else:
        HumanClient(ip, port).connect()

# Won't run if code is imported
if __name__ == '__main__':
    main()
