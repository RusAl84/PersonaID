from subprocess import Popen

while True:
    filename="capture_streamer.py"
    print("\nStarting " + filename)
    p1 = Popen("python " + filename, shell=True)
    # p2 = Popen("python " + filename, shell=True)
    p1.wait()