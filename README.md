# Introduction:
I don't plan to continue working on this poor project due to lack of time. It was created for personal use and to help a few of my friends. I'm publishing it on GitHub because someone might find it useful even in its current low quality.<br />

# Plugin description:
This is a very simple and poorly written script that should help monitor the creation, deletion, and modification of files in specified directories. Its window can be closed while it continues to run in the system tray. The script does not save logs and stores up to 5,000 records within a single session. I have only tested it on Windows, but with some adjustments, it should be able to run on Unix systems.<br />

The application will only monitor the directories listed in `"/Config/Watchlist.txt"`. Some files and directories can also be added to the exclusion list using the `"/Config/IgnoreWatchlist.txt"` file (these exclusions are either simple paths or RegExp). The `"/Config/Settings.txt"` file specifies the localization and the program behavior.<br />
There are only two languages available: English and Russian. There are also parameters that determine which events to monitor. For example, if the parameter `"ignore_modified: true"` is added, then the application will only notify about created, deleted or renamed files and directories. The available options for settings are listed in the section with **[Example of "Settings.txt"](https://github.com/Japanese-Schoolgirl/Simple-Directory-Overseer?tab=readme-ov-file#example-of-settingstxt)**.<br />

Many elements of the program are hardcoded, but I hope the script is at least somewhat readable and that you will be able to make your own edits to it if necessary. Good luck and have a nice day.<br />

### Preview:
![Preview](https://github.com/Japanese-Schoolgirl/Simple-Directory-Overseer/blob/main/%23Previews/Overall.png)

# Installation on Windows (from source):
1) Python 3.9+ (along with **pip** and **tkinter**) must be installed;<br />
2) Launch `"setup venv.bat"`;<br />
3) After second step you will be able to use `"start.bat"`;<br />
4) Edit file `"/Config/Watchlist.txt"` by adding specified directories.<br />

# Example of "Watchlist.txt":
```
C:\
D:\Steam\userdata\
```
**All of the listed paths must exist** on your system, otherwise the script will fail.

# Example of "IgnoreWatchlist.txt":
```
C:\Windows\Prefetch\
C:\Windows\ServiceState\EventLog\
C:\Windows\System32\config\systemprofile\
C:\Windows\servicing\
RegExp: (?i)\.cat$
RegExp: C:\\ProgramData\\NVIDIA Corporation\\Drs\\nvAppTimestamps$
C:\ProgramData\NVIDIA Corporation\Downloader\
```

# Example of "Settings.txt":
```
language: en
ignore_created: false
ignore_deleted: false
ignore_modified: false
ignore_moved: false
```