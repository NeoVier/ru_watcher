# ru_watcher

ru_watcher is a script to get the menu for a given day in [UFSC's Restaurante Universitário](https://ru.ufsc.br).

## Getting started

To get the program, you can just run 
```
git clone https://github.com/NeoVier/ru_watcher/
```

## Usage

To run, you can either run
```
python ru_watcher.py {date}
```
or you can symlink with
```
ln -s /path/to/ru_watcher.py/ /destination/path/new_name
```
where
```
/destination/path/
```
is a path that appears when you run
```
echo $PATH
```
and run
```
chmod +x /destionation/path/new_name
```
This will let you call ru_watcher anywhere in your system simply by entering the command (assuming the #! line correctly points to your python installation)
```
new_name {date}
```

To see the arguments the program accepts you can either run it without any arguments or with "help" as the first argument.
