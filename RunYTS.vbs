Dim objShell
Dim PythonExe
Dim PythonScript

Set objShell = CreateObject("Wscript.shell")

PythonExe = "python3 "
PythonScript = """C:\Users\rlau0\Documents\Parselmouth\yts\YTS.py"""

objShell.Run "cmd /k " & PythonExe & PythonScript