import cx_Freeze
import os

executables = [cx_Freeze.Executable("main.py")]

player = 'F:/Giereczka/Resources/Mobs/Player'

cx_Freeze.setup(
    name = "Giereczka",
    options={"build_exe": {"packages": ["pygame"],
                           "include_files": [os.path.join(player, 'player_stoi_prawo1.png'), os.path.join(player, 'player_stoi_prawo2.png'), os.path.join(player, 'player_stoi_prawo3.png'),
                                                os.path.join(player, 'player_stoi_lewo1.png'), os.path.join(player, 'player_stoi_lewo2.png'), os.path.join(player, 'player_stoi_lewo3.png'),
                                                os.path.join(player, 'player_idzie_lewo1.png'), os.path.join(player, 'player_idzie_lewo2.png'), os.path.join(player, 'player_idzie_lewo3.png'),
                                                os.path.join(player, 'player_idzie_prawo1.png'), os.path.join(player, 'player_idzie_prawo2.png'), os.path.join(player, 'player_idzie_prawo3.png'),
                                               'Resources/Mobs/default.png', 'Resources/b.jpg']}},
    executables = executables
)