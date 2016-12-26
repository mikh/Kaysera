#Wrapper for run script to make functions easier

import os
import sys

from Digital_Library.lib import arg_lib
from Digital_Library.lib import const_lib
from Digital_Library.lib import path_lib

module = 'kaysera'

path = const_lib.load_module_paths(module)
const = const_lib.load_module_const(module, private=True)


#Runs the script
#@input bash_shell<string>: Path to bash shell
#@input mapfile<string>: Map file to use
#@input player<string>: Robot to use for both players
#@input player1<string>: Robot to use for player 1
#@input player2<string>: Robot to use for player 2
#@input iterations<string>: Number of game iterations to run
#
def _run(bash_shell, mapfile, player, player1, player2, iterations, headless, random):
	robots_folder = 'bots'
	maps_folder = 'maps'
	iterations = int(iterations)
	if player != '':
		player1 = player
		player2 = player

	if not arg_lib.verify_arguments(bash_shell, mapfile, player1, player2) or iterations == 0:
		print("Please ensure bash_shell, mapfile, players, and iterations are set correctly")
		sys.exit(-1)

	map_path = os.path.join(maps_folder, mapfile + '.py')
	player1_path = os.path.join(robots_folder, player1, 'robot.py')
	player2_path = os.path.join(robots_folder, player2, 'robot.py')
	if not path_lib.file_exists(map_path) or not path_lib.file_exists(player1_path) or not path_lib.file_exists(player2_path):
		print("Please ensure map, and players are correctly named")
		sys.exit(-1)

	base_path = path_lib.get_directory(os.path.realpath(__file__))
	script_path = os.path.join(base_path, "tmp.sh")

	r_flag = ''
	h_flag = ''

	if random:
		r_flag = '-r'
	if headless:
		h_flag = '-H'

	print(script_path)
	with open(script_path, 'w') as f:
		f.write('PYTHONPATH="{}"\n'.format(const.pythonpath.new))
		f.write('export PYTHONPATH\n')
		f.write('{python27} {script_path} -m {map_path} {player1} {player2} -c {iterations} {random_flag} {headless_flag}\n'.format(python27 = path.python_27, script_path = path.rgkit, map_path=map_path.replace('\\', '/'), player1=player1_path.replace('\\', '/'), player2=player2_path.replace('\\', '/'), iterations=iterations, random_flag=r_flag, headless_flag=h_flag))
		f.write('PYTHONPATH="{}"\n'.format(const.pythonpath.current))
		f.write('export PYTHONPATH\n')

	command = '""{bash}" "{script}""'.format(bash=path.bash, script=script_path)
	os.system(command)

	path_lib.delete_file(script_path)





#ARGUMENT PARSING CODE

mapfile = 'default'

description = 'Wrapper for run script to make functions easier'

arg_vars = {
	'bash_shell': {'help': 'Path to bash shell', 'value': path.bash},
	'mapfile': {'help': 'Map file to use', 'value': mapfile},
	'player': {'help': 'Robot to use for both players', 'value': ''},
	'player1': {'help': 'Robot to use for player 1', 'value': ''},
	'player2': {'help': 'Robot to use for player 2', 'value': ''},
	'iterations': {'help': 'Number of game iterations to run', 'value': 1}
}

flag_vars = {
	'headless': {'help': 'Disable rendering game output', 'value': False},
	'random': {'help': 'Use random spawning.', 'value': False}
}

arg_parser = arg_lib.ArgumentController(description=description, set_variables=arg_vars, flag_variables=flag_vars)
var_data = arg_parser.parse_args()
if var_data != None:
	_run(**var_data)