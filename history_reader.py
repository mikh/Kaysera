#Script that reads the history

import os
import json
import sys

from Digital_Library.lib import path_lib

def save_history():
	files = path_lib.get_all_files_in_directory('history')

	index = 0

	for file in files:
		i = int(file.split('.')[1])
		if index < i:
			index = i + 1
	path_lib.copy_file('history.json', os.path.join('history', 'history.{}.json'.format(index)))
