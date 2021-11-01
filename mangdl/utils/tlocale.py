import locale
import os

"""uhh yea, this is one of the test files cuz i want to automatically detect the locale of the user and set it to the default
tl language"""

if os.name != 'posix':
	import ctypes
	lc = locale.windows_locale[ctypes.windll.kernel32.GetUserDefaultUILanguage()][:2]
else:
	lc = locale.getdefaultlocale()[0][:2]

print(lc)
