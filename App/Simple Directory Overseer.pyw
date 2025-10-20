""" This simple app wrote for personal needs by Japanese Schoolgirl (Lisa) """
# Python modules
import sys
import os
import subprocess
import time
import datetime
import PIL.Image
import PIL.ImageTk
import threading
import pystray
import tkinter as tk
from watchdog.observers import Observer as wdObserver
from watchdog.events import FileSystemEventHandler as wdFileSystemEventHandler

#################### Run as Administrator ####################
#if not pyuac.isUserAdmin():
#	try:
#		print("Requesting administrative privileges...")
#		pyuac.runAsAdmin(wait=False)
#		os._exit(0)
#	finally:
#		os._exit(0)
#################### Run as Administrator ####################

  ##~~~~~~~~~~~~~~~~~~# Core variables #~~~~~~~~~~~~~~~~~~##
appTitleName = r"Simple Directory Overseer"
osType = os.name
appPath = os.path.realpath(sys.argv[0])
appPathFolder = os.path.dirname(sys.argv[0]) # or "__file__"

appPathIcon = os.path.abspath(os.path.join(os.path.dirname(appPathFolder), 'App', 'icon.png'))
IMG_TrayIcon = PIL.Image.open(rf'{appPathIcon}')

appPathConfig = os.path.abspath(os.path.join(os.path.dirname(appPathFolder), 'Config'))
with open(os.path.join(appPathConfig, 'Watchlist.txt'), mode='r', encoding='utf_8') as f:
	_List = [line.strip() for line in f.readlines()] # Array which should contain "os.path.sep" at end
with open(os.path.join(appPathConfig, 'IgnoreWatchlist.txt'), mode='r', encoding='utf_8') as f:
	_IgnoreList = [line.strip() for line in f.readlines()]
with open(os.path.join(appPathConfig, 'language.txt'), mode='r', encoding='utf_8') as f:
	osLanguage = f.readline().strip('\n') # "en" or "ru"

TasksForDirectories = {}

  ##~~~~~~~~~~~~~~~~~~# Menus Labels #~~~~~~~~~~~~~~~~~~##
LabelExit = "Выйти из программы" if osLanguage == "ru" else "Exit the program"
LabelReload = "Перезапустить эту программу" if osLanguage == "ru" else "Restart this program"
LabelCloseGUI = "Прикрыть окно программы" if osLanguage == "ru" else "Withdraw program's window"
LabelOpenGUI = "Показать окно программы" if osLanguage == "ru" else "Show program's window"

  ##~~~~~~~~~~~~~~~~~~# Labels #~~~~~~~~~~~~~~~~~~##
LabelForCreate = " Создано: " if osLanguage == "ru" else " Created: "
LabelForDelete = " Удалено: " if osLanguage == "ru" else " Deleted: "
LabelForModify = " Изменено: " if osLanguage == "ru" else " Modified: "

  ##~~~~~~~~~~~~~~~~~~# Style #~~~~~~~~~~~~~~~~~~##
ColorGreen = { 'color': '#00ff00', 'tag': 'Green' }
ColorRed = { 'color': '#ff0000', 'tag': 'Red' }
ColorYellow = { 'color': '#ffff00', 'tag': 'Yellow' }

  ##~~~~~~~~~~~~~~~~~~# Main Menus Functions #~~~~~~~~~~~~~~~~~~##
def stopAll():
	try:
		for path in _List:
			TasksForDirectories[path].stop()
			TasksForDirectories[path].join()
		TrayApp.stop()
		rootGUI.destroy()
	finally:
		os._exit(0)

def startAll():
	for path in _List:
		# [!] this is probably a very cursed part, but it's good that I know almost nothing about Python, so I will not understand a extent of the horror
		global TasksForDirectories
		TasksForDirectories[path] = directoriesTask(path) # Path should exist
		TasksForDirectories[path].start()
	ThreadTrayApp.start()
	rootGUI.mainloop()

def ExitFunc():
	stopAll()
	os._exit(0)

def ReloadFunc():
	if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
		#updateTextArea("Running via PyInstaller", ColorRed['tag'])
		subprocess.Popen([sys.executable])
	else:
		subprocess.Popen([sys.executable, appPath]) # sys.executable will return current Python interpreter
	stopAll() # [!] maybe this part doesn't work properly, but so far I haven't noticed any problems, so I'll hope that there aren't any
	os._exit(0)

def GUI_Open():
	rootGUI.deiconify()
	rootGUI.lift()

def GUI_Close():
	rootGUI.withdraw()

def updateTextArea(insertLabel, colorTag = ColorRed['tag']):
	#print(insertLabel)
	#print(rootGUI.text_area.index('end-1c').split('.')[0])

	rootGUI.text_area.configure(state='normal')
	# Remove line if lines reach limit of 5 000
	if int(rootGUI.text_area.index('end-1c').split('.')[0]) > 5000:
		rootGUI.text_area.delete(1.0, 2.0)
	rootGUI.text_area.insert(tk.END, insertLabel, colorTag)
	rootGUI.text_area.configure(state='disabled')
	# Automatically scroll to last line
	rootGUI.text_area.see(tk.END)

def currentTime():
	return '[' + datetime.datetime.now().strftime('%H:%M:%S') + ']'

def fixPath(path):
	if os.path.isdir(path):
		return os.path.normpath(path) + os.path.sep
	else:
		return os.path.normpath(path)

def isIgnored(path):
	#print(_IgnoreList)
	#print(fixPath(path))
	#print(fixPath(path).startswith(tuple(_IgnoreList)))
	return fixPath(path).startswith(tuple(_IgnoreList))


  ##~~~~~~~~~~~~~~~~~~# Code for Tray #~~~~~~~~~~~~~~~~~~##
TrayAppMenu = pystray.Menu(
	# Adds items in menu ("default=True" adds bold style and triggers it on click) #
	pystray.MenuItem(LabelOpenGUI, GUI_Open, default=True),
	pystray.MenuItem(LabelCloseGUI, GUI_Close),
	pystray.Menu.SEPARATOR,
	pystray.MenuItem(LabelReload, ReloadFunc),
	pystray.Menu.SEPARATOR,
	pystray.MenuItem(LabelExit, ExitFunc)
)

TrayApp = pystray.Icon(f'Default', IMG_TrayIcon, appTitleName, menu=TrayAppMenu)
ThreadTrayApp = threading.Thread(target=TrayApp.run, daemon=True)

  ##~~~~~~~~~~~~~~~~~~# Code for Directories #~~~~~~~~~~~~~~~~~~##
class directoriesHandler(wdFileSystemEventHandler):
	def on_created(self, event) -> None:
		#return super().on_created(event)
		if not isIgnored(event.src_path):
			updateTextArea(currentTime() + LabelForCreate + fixPath(event.src_path) + "\n", ColorGreen['tag'])
		return None
	def on_deleted(self, event) -> None:
		if not isIgnored(event.src_path):
			updateTextArea(currentTime() + LabelForDelete + fixPath(event.src_path) + "\n", ColorRed['tag'])
		return None
	def on_modified(self, event) -> None:
		if not isIgnored(event.src_path):
			updateTextArea(currentTime() + LabelForModify + fixPath(event.src_path) + "\n", ColorYellow['tag'])
		return None

def directoriesTask(directory):
	pathObserver = wdObserver()
	pathObserver.schedule(directoriesHandler(), directory, recursive=True)
	return pathObserver

  ##~~~~~~~~~~~~~~~~~~# Code for GUI #~~~~~~~~~~~~~~~~~~##
rootGUI = tk.Tk()
rootGUI.title(appTitleName)
rootGUI.iconphoto(False, PIL.ImageTk.PhotoImage(IMG_TrayIcon))
rootGUI.protocol('WM_DELETE_WINDOW', GUI_Close)
rootGUI.configure(background = 'purple')
rootGUI.minsize(800, 300)

# Create text field
rootGUI.text_area = tk.Text(rootGUI, font=('Arial', 8), state='disabled', width=40, height=10)
rootGUI.text_area.pack(fill='both', expand=True)
rootGUI.text_area.pack(padx=4, pady=4)

rootGUI.text_area.configure(background = 'black')
rootGUI.text_area.tag_configure(ColorGreen['tag'], foreground = ColorGreen['color'])
rootGUI.text_area.tag_configure(ColorRed['tag'], foreground = ColorRed['color'])
rootGUI.text_area.tag_configure(ColorYellow['tag'], foreground = ColorYellow['color'])

GUIscrollbar = tk.Scrollbar(rootGUI, command=rootGUI.text_area.yview)
rootGUI.text_area.config(yscrollcommand=GUIscrollbar.set)
rootGUI.text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
GUIscrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Create text for GUI from array
#text_array = [
#	"123",
#	"456",
#	"789."
#]
#for line in text_array:
#	rootGUI.text_area.insert(tk.END, line + "\n")

  ##~~~~~~~~~~~~~~~~~~# Code #~~~~~~~~~~~~~~~~~~##
def main():
	try:
		while True:
			time.Sleep(1)
	#except KeyboardInterrupt:
	finally:
		ExitFunc()

if __name__ == "__main__":
	startAll()
	main()