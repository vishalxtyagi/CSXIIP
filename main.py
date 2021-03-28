import functions as fn
from login import Login
from panel import Panel

if __name__ == '__main__':
    if fn.checkAuth():
        fn.start(Panel)
    else:
        fn.start(Login)
    