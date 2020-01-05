import cx_Freeze

executables = [cx_Freeze.Executable("main.py")]

cx_Freeze.setup(
    name = "Giereczka",
    options={"build_exe": {"packages": ["pygame"],
                           "include_files": ['Resources/Mobs/goblin_lewo.png', 'Resources/Mobs/goblin_prawo.png',
                                               'Resources/Mobs/player1.png', 'Resources/Mobs/player2.png', 'Resources/Mobs/player3.png',
                                               'Resources/Mobs/default.png', 'Resources/b.jpg']}},
    executables = executables
)