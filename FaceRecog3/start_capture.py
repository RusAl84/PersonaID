from subprocess import Popen

while True:
    filename="capture_pg.py"
    print("\nStarting " + filename)
    p = Popen("python " + filename, shell=True)
    p.wait()