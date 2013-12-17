from cx_Freeze import setup, Executable
setup(name="game",version="1",description="a game",executables=[Executable("./src/main.py")])