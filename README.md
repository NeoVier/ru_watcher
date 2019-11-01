#ru_watcher

ru_watcher is a script to get the menu for a given day in [UFSC's Restaurante Universitário](https://ru.ufsc.br) UFSC's Restaurante Universitario.

Usage

To run, you can either run "python ru_watcher.py {date}" or you can symlink with "ln -s /path/to/ru_watcher.py/ /destination/path/ru_watcher", where /destination/path/ is a path that appears when you do "echo $PATH" (you can also change the name ru_watcher to whatever you like) and do "chmod +x /destionation/path/ru_watcher". This will let you call ru_watcher anywhere in your system simply by entering the command "ru_watcher {date}" (assuming the #! line correctly points to your python installation)

To see the arguments the program accepts you can either run it without any arguments or with "help" as the first argument.
