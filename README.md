\# Windows Path Editor (Advanced)



A lightweight, graphical utility built with Python and wxPython to safely manage your Windows User Environment Variables (`PATH`). This tool allows you to add, delete, and—most importantly—reorder paths to manage executable priority with ease.



\## 🚀 Features



\*   \*\*Priority Management:\*\* Move paths up and down to change their execution priority (Top to Bottom).

\*   \*\*Safe Browsing:\*\* Use a folder picker to add new paths without typing errors.

\*   \*\*Keyboard Shortcuts:\*\*

&#x20;   \*   `Alt + Up`: Move selected path up.

&#x20;   \*   `Alt + Down`: Move selected path down.

&#x20;   \*   `Delete`: Remove selected path from the list.

\*   \*\*Live System Update:\*\* Automatically broadcasts a system change message after saving, so you don't need to restart your PC to see changes in most applications.

\*   \*\*Registry-Based:\*\* Works directly and safely with `HKEY\_CURRENT\_USER\\Environment`.



\## 🛠️ Prerequisites



To run this tool from source, you need:

\*   Python 3.x

\*   `wxPython` library



Install the required dependency via pip:

```bash

pip install wxpython

