import server
import webbrowser

if __name__ == '__main__':
    addr = 'localhost'
    webbrowser.open("http://%s:%s/"%(addr, server.SERVER_PORT), new=2,autoraise=True)