from subprocess import Popen

while True:
    filename="process.py"
    print("\nStarting " + filename)
    p = Popen("python " + filename, shell=True)
    p.wait()