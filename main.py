import time
from window import IsoWindow

def main():
    win = IsoWindow(800, 600, "Pyiso")
    last : int = time.time_ns()
    while not win.should_close():
        now : int = time.time_ns()
        win.poll_events()
        dt : float = (now - last) / 1000000000.0
        win.renderer.render(dt)
        last = now

    win.terminate()

if __name__=="__main__":
    main()
