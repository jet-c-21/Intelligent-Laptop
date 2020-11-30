import os
import ctypes
import platform


class UITool:
    @staticmethod
    def msg_window(title='', msg=''):
        if platform.system() == 'Windows':
            ctypes.windll.user32.MessageBoxW(0, msg, title, 0)
        else:
            cmd = f'''
            osascript -e 'Tell application "System Events" to display dialog "{msg}" with title "{title}"'
            '''
            os.system(cmd)
