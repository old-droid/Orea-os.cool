import os
import time
import random
import shutil
from datetime import datetime

class OreaOS:
    def __init__(self):
        self.current_dir = "/home/user"
        self.file_system = {
            "/": {
                "bin": {},
                "etc": {
                    "apt": {},
                    "config": {}
                },
                "home": {
                    "user": {
                        "documents": {},
                        "downloads": {},
                        "pictures": {},
                        "projects": {
                            "python_app": {
                                "main.py": "print('Hello, world!')",
                                "requirements.txt": "requests==2.28.1\nnumpy==1.23.0"
                            }
                        }
                    }
                },
                "usr": {
                    "lib": {},
                    "share": {}
                },
                "var": {
                    "log": {}
                }
            }
        }
        self.running = True
        self.command_history = []
        self.bg_color = (0, 10, 0)  # Dark green background
        self.text_color = (0, 255, 0)  # Bright green text
        self.font = "Monospace"
        self.commands = {
            "ls": self.ls,
            "pwd": self.pwd,
            "cd": self.cd,
            "mkdir": self.mkdir,
            "rmdir": self.rmdir,
            "rm": self.rm,
            "cp": self.cp,
            "mv": self.mv,
            "touch": self.touch,
            "file": self.file_info,
            "zip": self.zip_files,
            "unzip": self.unzip_files,
            "tar": self.tar_files,
            "nano": self.nano,
            "vi": self.vi,
            "jed": self.jed,
            "cat": self.cat,
            "tac": self.tac,
            "chmod": self.chmod,
            "apt": self.apt,
            "dnf": self.dnf,
            "exit": self.exit,
            "help": self.help,
            "clear": self.clear,
            "date": self.date,
            "whoami": self.whoami,
            "echo": self.echo,
            "grep": self.grep,
            "find": self.find,
            "neofetch": self.neofetch
        }
    
    def get_path_contents(self, path):
        parts = path.strip('/').split('/')
        current = self.file_system['/']
        
        for part in parts:
            if part:
                if part in current:
                    current = current[part]
                else:
                    return None
        
        return current
    
    def path_exists(self, path):
        return self.get_path_contents(path) is not None
    
    def display_prompt(self):
        username = "user"
        hostname = "orea"
        return f"\033[1;32m{username}@{hostname}\033[0m:\033[1;34m{self.current_dir}\033[0m$ "
    
    def process_command(self, input_cmd):
        if not input_cmd.strip():
            return
        
        self.command_history.append(input_cmd)
        parts = input_cmd.split()
        cmd = parts[0]
        args = parts[1:] if len(parts) > 1 else []
        
        if cmd in self.commands:
            try:
                self.commands[cmd](args)
            except Exception as e:
                print(f"Error executing command: {e}")
        else:
            print(f"Command not found: {cmd}. Type 'help' for available commands.")
    
    # Command implementations
    def ls(self, args):
        target_path = args[0] if args else self.current_dir
        contents = self.get_path_contents(target_path if target_path.startswith('/') else f"{self.current_dir}/{target_path}")
        
        if contents is None:
            print(f"ls: cannot access '{target_path}': No such file or directory")
            return
            
        # Handle flags like -l, -a, etc.
        show_hidden = "-a" in args
        long_format = "-l" in args
        
        items = list(contents.keys())
        items.sort()
        
        if long_format:
            print("total", len(items))
            for item in items:
                if item.startswith('.') and not show_hidden:
                    continue
                    
                is_dir = isinstance(contents[item], dict)
                permissions = "drwxr-xr-x" if is_dir else "-rw-r--r--"
                size = len(str(contents[item])) if not is_dir else 4096
                date = "Feb 27 14:30"
                print(f"{permissions} 1 user group {size:8} {date} {item}")
        else:
            for item in items:
                if item.startswith('.') and not show_hidden:
                    continue
                    
                if isinstance(contents[item], dict):
                    print(f"\033[1;34m{item}/\033[0m", end="  ")
                else:
                    print(item, end="  ")
            print()
    
    def pwd(self, args):
        print(self.current_dir)
    
    def cd(self, args):
        if not args:
            self.current_dir = "/home/user"
            return
            
        target = args[0]
        
        if target == "..":
            if self.current_dir != "/":
                self.current_dir = "/".join(self.current_dir.split("/")[:-1])
                if self.current_dir == "":
                    self.current_dir = "/"
        elif target == "~":
            self.current_dir = "/home/user"
        elif target.startswith("/"):
            if self.path_exists(target):
                self.current_dir = target
            else:
                print(f"cd: {target}: No such file or directory")
        else:
            new_path = f"{self.current_dir}/{target}" if self.current_dir != "/" else f"/{target}"
            if self.path_exists(new_path):
                self.current_dir = new_path
            else:
                print(f"cd: {target}: No such file or directory")
    
    def mkdir(self, args):
        if not args:
            print("mkdir: missing operand")
            return
            
        for target in args:
            if target.startswith("/"):
                parent_path = "/".join(target.split("/")[:-1])
                dir_name = target.split("/")[-1]
                parent = self.get_path_contents(parent_path)
            else:
                parent = self.get_path_contents(self.current_dir)
                dir_name = target
                
            if parent is not None:
                if dir_name in parent and isinstance(parent[dir_name], dict):
                    print(f"mkdir: cannot create directory '{target}': File exists")
                else:
                    parent[dir_name] = {}
            else:
                print(f"mkdir: cannot create directory '{target}': No such file or directory")
    
    def rmdir(self, args):
        if not args:
            print("rmdir: missing operand")
            return
            
        for target in args:
            if target.startswith("/"):
                parent_path = "/".join(target.split("/")[:-1])
                dir_name = target.split("/")[-1]
                parent = self.get_path_contents(parent_path)
            else:
                parent = self.get_path_contents(self.current_dir)
                dir_name = target
                
            if parent is not None and dir_name in parent:
                if isinstance(parent[dir_name], dict):
                    if not parent[dir_name]:  # Check if empty
                        del parent[dir_name]
                    else:
                        print(f"rmdir: failed to remove '{target}': Directory not empty")
                else:
                    print(f"rmdir: failed to remove '{target}': Not a directory")
            else:
                print(f"rmdir: failed to remove '{target}': No such file or directory")
    
    def rm(self, args):
        if not args:
            print("rm: missing operand")
            return
            
        recursive = "-r" in args or "-rf" in args
        args = [arg for arg in args if not arg.startswith("-")]
        
        for target in args:
            if target.startswith("/"):
                parent_path = "/".join(target.split("/")[:-1])
                item_name = target.split("/")[-1]
                parent = self.get_path_contents(parent_path)
            else:
                parent = self.get_path_contents(self.current_dir)
                item_name = target
                
            if parent is not None and item_name in parent:
                if isinstance(parent[item_name], dict) and not recursive:
                    print(f"rm: cannot remove '{target}': Is a directory")
                else:
                    del parent[item_name]
            else:
                print(f"rm: cannot remove '{target}': No such file or directory")
    
    def cp(self, args):
        if len(args) < 2:
            print("cp: missing file operand")
            return
            
        source = args[0]
        dest = args[1]
        
        source_content = self.get_path_contents(source if source.startswith('/') else f"{self.current_dir}/{source}")
        if source_content is None:
            print(f"cp: cannot stat '{source}': No such file or directory")
            return
            
        # Simplified implementation
        print(f"Copied {source} to {dest}")
    
    def mv(self, args):
        if len(args) < 2:
            print("mv: missing file operand")
            return
            
        source = args[0]
        dest = args[1]
        
        # Simplified implementation
        print(f"Moved {source} to {dest}")
    
    def touch(self, args):
        if not args:
            print("touch: missing file operand")
            return
            
        for target in args:
            if target.startswith("/"):
                parent_path = "/".join(target.split("/")[:-1])
                file_name = target.split("/")[-1]
                parent = self.get_path_contents(parent_path)
            else:
                parent = self.get_path_contents(self.current_dir)
                file_name = target
                
            if parent is not None:
                if file_name not in parent:
                    parent[file_name] = ""
            else:
                print(f"touch: cannot touch '{target}': No such file or directory")
    
    def file_info(self, args):
        if not args:
            print("file: missing file operand")
            return
            
        target = args[0]
        content = self.get_path_contents(target if target.startswith('/') else f"{self.current_dir}/{target}")
        
        if content is None:
            print(f"file: cannot open '{target}' (No such file or directory)")
        elif isinstance(content, dict):
            print(f"{target}: directory")
        else:
            print(f"{target}: ASCII text")
    
    def zip_files(self, args):
        if len(args) < 2:
            print("zip: missing file operand")
            return
            
        zip_name = args[0]
        files = args[1:]
        print(f"Adding files to {zip_name}...")
        for file in files:
            print(f"  adding: {file}")
    
    def unzip_files(self, args):
        if not args:
            print("unzip: missing file operand")
            return
            
        zip_name = args[0]
        print(f"Extracting files from {zip_name}...")
    
    def tar_files(self, args):
        if not args:
            print("tar: missing file operand")
            return
            
        # Simplified implementation
        print("Creating tar archive...")
    
    def nano(self, args):
        if not args:
            print("nano: missing file operand")
            return
            
        file_name = args[0]
        print(f"Opening {file_name} in nano editor...")
        time.sleep(1)
        print("Exit nano with Ctrl+X")
    
    def vi(self, args):
        if not args:
            print("vi: missing file operand")
            return
            
        file_name = args[0]
        print(f"Opening {file_name} in vi editor...")
        time.sleep(1)
        print("Exit vi with :q!")
    
    def jed(self, args):
        if not args:
            print("jed: missing file operand")
            return
            
        file_name = args[0]
        print(f"Opening {file_name} in jed editor...")
        time.sleep(1)
        print("Exit jed with Ctrl+X")
    
    def cat(self, args):
        if not args:
            print("cat: missing file operand")
            return
            
        for file_name in args:
            content = self.get_path_contents(file_name if file_name.startswith('/') else f"{self.current_dir}/{file_name}")
            
            if content is None:
                print(f"cat: {file_name}: No such file or directory")
            elif isinstance(content, dict):
                print(f"cat: {file_name}: Is a directory")
            else:
                print(content)
    
    def tac(self, args):
        if not args:
            print("tac: missing file operand")
            return
            
        for file_name in args:
            content = self.get_path_contents(file_name if file_name.startswith('/') else f"{self.current_dir}/{file_name}")
            
            if content is None:
                print(f"tac: {file_name}: No such file or directory")
            elif isinstance(content, dict):
                print(f"tac: {file_name}: Is a directory")
            else:
                # Print content in reverse
                lines = content.split('\n')
                for line in reversed(lines):
                    print(line)
    
    def chmod(self, args):
        if len(args) < 2:
            print("chmod: missing operand")
            return
            
        # Simplified implementation
        print(f"Changed mode of {args[1]} to {args[0]}")
    
    def apt(self, args):
        if not args:
            print("apt: missing command")
            return
            
        if args[0] == "update":
            print("Reading package lists... Done")
        elif args[0] == "upgrade":
            print("Reading package lists... Done")
            print("Building dependency tree... Done")
            print("0 upgraded, 0 newly installed, 0 to remove and 0 not upgraded.")
        elif args[0] == "install":
            if len(args) < 2:
                print("apt: missing package name")
                return
                
            for package in args[1:]:
                print(f"Installing {package}...")
                time.sleep(0.5)
                print(f"{package} has been installed successfully")
        else:
            print(f"apt: invalid operation: {args[0]}")
    
    def dnf(self, args):
        # Similar to apt but for Fedora/RHEL
        print("DNF package manager (Fedora/RHEL)")
    
    def exit(self, args):
        print("Logging out...")
        self.running = False
    
    def help(self, args):
        print("Available commands:")
        commands = list(self.commands.keys())
        commands.sort()
        
        # Display in columns
        col_width = max(len(cmd) for cmd in commands) + 2
        cols = 4
        rows = (len(commands) + cols - 1) // cols
        
        for i in range(rows):
            line = ""
            for j in range(cols):
                idx = i + j * rows
                if idx < len(commands):
                    line += commands[idx].ljust(col_width)
            print(line)
    
    def clear(self, args):
        print("\033c", end="")
    
    def date(self, args):
        print(datetime.now().strftime("%a %b %d %H:%M:%S %Z %Y"))
    
    def whoami(self, args):
        print("user")
    
    def echo(self, args):
        print(" ".join(args))
    
    def grep(self, args):
        if len(args) < 2:
            print("grep: missing pattern and file operand")
            return
            
        pattern = args[0]
        files = args[1:]
        
        for file_name in files:
            content = self.get_path_contents(file_name if file_name.startswith('/') else f"{self.current_dir}/{file_name}")
            
            if content is None:
                print(f"grep: {file_name}: No such file or directory")
            elif isinstance(content, dict):
                print(f"grep: {file_name}: Is a directory")
            else:
                lines = content.split('\n')
                for line in lines:
                    if pattern in line:
                        print(line)
    
    def find(self, args):
        if not args:
            path = self.current_dir
            pattern = "*"
        elif len(args) == 1:
            path = args[0]
            pattern = "*"
        else:
            path = args[0]
            pattern = args[1]
            
        print(f"Finding files matching '{pattern}' in {path}")
    
    def neofetch(self, args):
        logo = """
 ██████  ██████  ███████  █████  
██    ██ ██   ██ ██      ██   ██ 
██    ██ ██████  █████   ███████ 
██    ██ ██   ██ ██      ██   ██ 
 ██████  ██   ██ ███████ ██   ██ 
                                 
"""
        print(logo)
        print(f"OS: Orea OS")
        print(f"Kernel: 5.15.0-orea")
        print(f"Uptime: {random.randint(1, 24)} hours, {random.randint(1, 59)} mins")
        print(f"Shell: bash 5.1.16")
        print(f"Resolution: 1920x1080")
        print(f"CPU: Intel i7-10700 (8) @ 3.80GHz")
        print(f"Memory: {random.randint(2000, 4000)}MiB / 8192MiB")

    def run(self):
        self.clear([])
        self.neofetch([])
        print("\nWelcome to Orea OS - A simulated OS for tech enthusiasts!")
        print("Type 'help' to see available commands.\n")
        
        while self.running:
            try:
                user_input = input(self.display_prompt())
                self.process_command(user_input)
            except KeyboardInterrupt:
                print("\nInterrupted. Use 'exit' to quit.")
            except EOFError:
                print("\nEOF detected. Exiting...")
                self.running = False

if __name__ == "__main__":
    os_instance = OreaOS()
    os_instance.run()
