'''
Python to .exe
Uses the cx_Freeze module to compile.
(http://cx-freeze.sourceforge.net/
http://www.lfd.uci.edu/~gohlke/pythonlibs/#cx_Freeze)

This was written to make the process of compiling done more by the computer.
by: beary605
'''
import subprocess, sys, os

#Get and process input...
a1=raw_input("Name of executable?\t")
b1=raw_input("Version number?\t")
c1=raw_input("Description?\t")
d1=raw_input("Python file?\t")
if a1=='': a1=d1.split('\\')[-1][:-3]

#Write the setup file...
f2=open('setup'+a1+'.py', 'w')
#print "Writing",'setup("'+a1+'","'+b1+'","'+c1+'",[Executable("'+d1+'")])',"to",'setup'+a1+'.py'
f2.write('from cx_Freeze import setup, Executable\n')
e2='setup(name="%s",version="%s",description="%s",executables=[Executable("%s")])' % (a1,b1,c1,d1)
f2.write(e2)
f2.close()

#File checking...
f3=open(d1, 'r')
e3=f3.read()
if (e3.find('from pygame')!=-1 or e3.find('import pygame')!=-1) and e3.find('import pygame._view')==-1:
    print "A pygame program needs to import pygame._view specifically."
    g3=raw_input("Let me modify your program to do so(Y/N)?\t")
    if g3 in ("Yy"):
        f3=open(d1, 'w')
        f3.write('import pygame._view\n')
        f3.write(e3)
        print "All Fixed!"
f3.close()

#Execute the setup file...
a4='python setup%s.py build' % a1
b4=raw_input("Want me to print all the debug data from the setup(Y/N)?")
if b4 in ("Yy"):
    process=subprocess.Popen(a4, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
else:
    process=subprocess.Popen(a4)

#Read the terminal text
if b4 in ("Yy"):
    while True: #StackOverflow, woot
        out = process.stdout.read(20) 
        if out == '' and process.poll() != None: 
            break 
        if out != '': 
            sys.stdout.write(out) 
            sys.stdout.flush()

#Remove the setup file?
a5=raw_input("Would you like to delete the setup file(Y/N)?")
if a5 in ("Yy"):
    os.remove('setup'+a5+'.py')

print """
If your Executable program still does not work:
    - Check to see that you compiled a Python program that itself doesn't crash.
    - Check to see if all the required files are there.
      For example, images that are loaded, text files that are read.
To check if your program works, or to retrieve debugging data, open CMD, and run the program."""
