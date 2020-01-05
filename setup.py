import cx_Freeze

executables = [cx_Freeze.Executable("main.py")]

player = 'F:/Giereczka/Resources/Mobs/Player'

cx_Freeze.setup(
    name = "Giereczka",
    options={"build_exe": {"packages": ["pygame"],
                      "include_files": ["Resources"]}},

    executables = executables
)