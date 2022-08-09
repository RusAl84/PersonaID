from subprocess import Popen

while True:
    filename="process.py"
    print("\nStarting " + filename)
    p1 = Popen("python " + filename, shell=True)
    p2 = Popen("python " + filename, shell=True)
    p3 = Popen("python " + filename, shell=True)
    p4 = Popen("python " + filename, shell=True)
    p1.wait()