import socketserver, threading, io, socket, code, sys, traceback

from .api_krita import Krita
from krita import Extension # type: ignore

PORT: int = 12174

class Shell(code.InteractiveConsole):
    _sockout: socket.SocketType

    def __init__(self, stdin, sockout):
        super().__init__({"print": self.print})
        self._stdin = stdin
        self._sockout = sockout

    def raw_input(self, prompt_ignored):
        return self._stdin.readline().rstrip()
    
    def print(self, *args, **kwargs):
        output = io.StringIO()
        print(*args, file=output, **kwargs)
        self.write(output.getvalue())
        output.close()

    def write(self, data):
        self._sockout.sendall(data.encode('utf-8'), socket.MSG_NOSIGNAL) # MSG_NOSIGNAL prevents Krita crashes

    # Copied from code.py, removed calls to system exception handlers
    def showtraceback(self):
        """Display the exception that just occurred.

        We remove the first stack item because it is our own code.

        The output is written by self.write(), below.

        """
        sys.last_type, sys.last_value, last_tb = ei = sys.exc_info()
        sys.last_traceback = last_tb
        sys.last_exc = ei[1]
        try:
            lines = traceback.format_exception(ei[0], ei[1], last_tb.tb_next)
            self.write(''.join(lines))
        finally:
            last_tb = ei = None

    # Copied from code.py, removed calls to system exception handlers
    def showsyntaxerror(self, filename=None):
        """Display the syntax error that just occurred.

        This doesn't display a stack trace because there isn't one.

        If a filename is given, it is stuffed in the exception instead
        of what was there before (because Python's parser always uses
        "<string>" when reading from a string).

        The output is written by self.write(), below.

        """
        type, value, tb = sys.exc_info()
        sys.last_exc = value
        sys.last_type = type
        sys.last_value = value
        sys.last_traceback = tb
        if filename and type is SyntaxError:
            # Work hard to stuff the correct filename in the exception
            try:
                msg, (dummy_filename, lineno, offset, line) = value.args
            except ValueError:
                # Not the format we expect; leave it alone
                pass
            else:
                # Stuff in the right filename
                value = SyntaxError(msg, (filename, lineno, offset, line))
                sys.last_exc = sys.last_value = value
        lines = traceback.format_exception_only(type, value)
        self.write(''.join(lines))


class RequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.request.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)
        self.stdin = self.request.makefile('r', -1)
        shell = Shell(self.stdin, self.request)
        try:
          shell.interact(banner='', exitmsg='')
        except Exception as e:
          # This is triggered when the client closes the connection
          pass

    def finish(self):
        self.stdin.close()
        self.request.close()

class ServerThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True

    def run(self):
        with socketserver.ThreadingTCPServer(('localhost', PORT), RequestHandler) as server:
            server.daemon_threads = True
            server.allow_reuse_address = True
            server.serve_forever()
        

class KritaLocalhostExtension(Extension):
    _server_thread: ServerThread

    def __init__(self, parent):
        super().__init__(parent)

    def setup(self):
        self._server_thread = ServerThread()
        self._server_thread.start()

    def createActions(self, window):
        pass

Krita.add_extension(KritaLocalhostExtension)
