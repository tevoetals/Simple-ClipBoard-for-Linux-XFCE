Simple Clipboard Manager for Linux (XFCE & Others)

Overview

This is a lightweight clipboard manager designed to run in the background on Linux (XFCE and other environments). It enhances clipboard functionality by allowing users to quickly access and manage copied items.

How it Works

Any text copied will be stored in the clipboard history.
Paste with Ctrl + Alt + V: Opens a selection window with clipboard history.
Select an item: Navigate using arrow keys or mouse clicks.
Paste: Press Enter or Space to paste the selected item.

Installation

Before running the script, ensure you have the required dependencies installed. You can install them using pip:

pip install pynput

Additionally, Tkinter and subprocess are standard Python modules, but make sure you have them installed. For Debian/Ubuntu-based systems, you may need to install python3-tk:

sudo apt install python3-tk
