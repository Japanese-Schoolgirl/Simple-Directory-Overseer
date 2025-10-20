# Introduction:
I don't plan to continue working on this poor project due to lack of time. It was created for personal use and to help a few of my friends. I'm publishing it on Git because someone might find it useful even in its current low quality.<br />

# Plugin description:
This is very simple and poorly written script, which should help monitor the creation, deletion, and modification of files in desired directories. Its window can be closed, and it will continue to run in the tray. The script does not save logs and stores up to 5,000 records within a single session. I have only tested it on Windows, but with some adjustments, it should be able to run on Unix systems.<br />
The application will only monitor the directories specified in `“/Config/Watchlist.txt”`. Some directories can also be added to the exclusion list using the `“/Config/IgnoreWatchlist.txt”` file. The `“/Config/language.txt”` file specifies the localization. There are only two languages available: English and Russian. Many elements of the program are hardcoded, but I hope the script is at least somewhat readable and that you will be able to make your own edits to it if necessary. Good luck and have a nice day.<br />
### Preview:
![Preview](https://github.com/Japanese-Schoolgirl/Simple-Directory-Overseer/blob/main/%23Previews/Overall.png)

# Installation on Windows (from source):
1) Python 3.9+ (along with **pip** and **tkinter**) must be installed;<br />
2) Launch `"setup venv.bat"`;<br />
3) After second step you will be able to use `"start.bat"`;<br />
4) Edit file `"/Config/Watchlist.txt"` by adding desired directories.<br />

# Example of "Watchlist.txt":
```
C:\
D:\Steam\userdata\
```

# Example of "IgnoreWatchlist.txt":
```
C:\Windows\Prefetch\
C:\Windows\ServiceState\EventLog\
C:\Windows\System32\config\systemprofile\
C:\Windows\servicing\
C:\ProgramData\NVIDIA Corporation\Drs\nvAppTimestamps\
```