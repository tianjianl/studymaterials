import pywebcopy
from pywebcopy import save_website

kwargs = {'project_name': 'level1'} # it will create a folder in desired folder with name 'talalsite'

save_website(
    url='https://xss-game.appspot.com/level1',
    project_folder='/Users/litianjian/Documents/GitHub/studymaterials/level1',
    **kwargs
)
