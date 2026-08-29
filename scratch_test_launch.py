import os
import sys

mario_dir = os.path.abspath('Mario-AI-Framework')
bin_dir = os.path.join(mario_dir, 'bin')
cp = bin_dir + ';' + os.path.join(bin_dir, '*')
lvl = os.path.join(mario_dir, 'levels', 'level_0.txt')

bat_content = f'''@echo off
cd /d "{mario_dir}"
java -cp "{cp}" PlayLevel "{lvl}" play 0 0 3 0
exit
'''

bat_path = os.path.join(mario_dir, 'run_game.bat')
with open(bat_path, 'w') as f:
    f.write(bat_content)

os.startfile(bat_path)
print("Successfully launched batch file via os.startfile!")
