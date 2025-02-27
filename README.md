# OreaOS - Terminal Operating System Simulator

A Python-based terminal operating system simulator that provides a realistic Unix-like command-line experience for learning and experimentation.

![OreaOS Logo](https://raw.githubusercontent.com/old-droid/oreaos/main/assets/logo.png)

## 🌟 Features

- **Realistic File System**: In-memory hierarchical file system with standard Unix directory structure
- **30+ Unix-like Commands**: Implementation of common terminal commands like `ls`, `cd`, `mkdir`, etc.
- **Package Management**: Simulated `apt` and `dnf` package managers
- **Text Editors**: Basic simulations of `nano`, `vi`, and `jed`
- **File Operations**: Complete set of file manipulation commands (`cp`, `mv`, `rm`, etc.)
- **System Information**: `neofetch`-style system information display
- **Retro Terminal Style**: Green-on-black classic terminal aesthetics

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- Terminal emulator with ANSI color support

### Installation

1. Clone the repository:
```bash
git clone https://github.com/old-droid/oreaos.git
cd oreaos
```

2. Run the simulator:
```bash
python main.py
```

## 🛠️ Available Commands

OreaOS supports the following commands:

### File Operations
- `ls` - List directory contents
- `pwd` - Print working directory
- `cd` - Change directory
- `mkdir` - Create directory
- `rmdir` - Remove directory
- `rm` - Remove files/directories
- `cp` - Copy files
- `mv` - Move files
- `touch` - Create empty files

### File Manipulation
- `cat` - Display file contents
- `tac` - Display file contents in reverse
- `grep` - Search text in files
- `find` - Search for files
- `chmod` - Change file permissions

### Archive Operations
- `zip` - Create ZIP archives
- `unzip` - Extract ZIP archives
- `tar` - Handle TAR archives

### Text Editors
- `nano` - Simple text editor
- `vi` - Vi text editor simulation
- `jed` - Jed editor simulation

### System Commands
- `neofetch` - Display system information
- `date` - Show current date/time
- `whoami` - Show current user
- `clear` - Clear terminal screen
- `exit` - Exit the simulator

### Package Management
- `apt` - Advanced Package Tool (Debian-style)
- `dnf` - DNF Package Manager (Fedora-style)

## 📁 File System Structure

```
/
├── bin/
├── etc/
│   ├── apt/
│   └── config/
├── home/
│   └── user/
│       ├── documents/
│       ├── downloads/
│       ├── pictures/
│       └── projects/
├── usr/
│   ├── lib/
│   └── share/
└── var/
    └── log/
```

## 🎨 Customization

The simulator's appearance can be customized by modifying these properties in the `OreaOS` class:

```python
self.bg_color = (0, 10, 0)     # Dark green background
self.text_color = (0, 255, 0)  # Bright green text
self.font = "Monospace"
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by Unix-like operating systems
- Terminal color schemes inspired by classic green phosphor monitors
- Command implementations based on GNU coreutils

## 📞 Contact

- GitHub: [@old-droid](https://github.com/old-droid)
- Project Link: [https://github.com/old-droid/oreaos](https://github.com/old-droid/oreaos)

