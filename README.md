# 🐧 Linux Command Manual Generator (Python Project)

This project is a Python-based CLI tool that helps generate, manage, and verify command documentation files for common **Linux/Unix commands**. It uses shell utilities, XML serialization, and file comparison techniques to automate manual generation.


---

## 🚀 Features

- **View Commands**  
  Display a menu of predefined Linux commands.

- **Generate XML Manuals**  
  Automatically create XML files for each command, including:
  - Description
  - Version history
  - Example usage
  - Related commands
  - Syntax & documentation links

- **Search Command Manuals**  
  Lookup any command and display its generated XML file.

- **Verify Manual Files**  
  Compare original XML with its copied version to detect modifications.

- **Command Recommendation**  
  Suggest most recently used commands from `.bash_history`.

---

## 🛠 Technologies Used

- Python 3
- `subprocess`, `os`, `shutil`
- `xml.etree.ElementTree`, `minidom`
- `difflib` for verification
- Shell commands (`man`, `grep`, `awk`, etc.)

---


