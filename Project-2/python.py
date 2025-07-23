import difflib
import subprocess
import os
import shutil
import xml.etree.ElementTree as ET
from xml.dom import minidom

class CommandManual:
    command_examples = {
        "cat": "echo 'cat file  The result is Display what is in the file assume in have abood if have in abood abood and abed cat abood the result abood and abed '",
        "nano": "echo 'nano file that creates any type of file  txt, c ...  '",
        "mv": "echo 'mv file.txt file1 .txt or mv oldfile.txt new file renames oldfile'",
        "ls": "echo ' ls -l show all data for file ls Desktop '",
        "touch": "echo 'touch newfile.txt creates new empty file touch yes '", 
        "mkdir": "echo 'mkdir newDirectory creates a new directory folder named newDirectory'",
        "pico": "echo 'pico newfile.txt test editor  creating or editing a file name is newfile'",
        "cp": "echo 'cp abood abood1 and using cat display abood one data to abood two'",
        "sed": "echo 'numberlin one numberline two output it show just line between and numberline one to numberline two '",
        "grep": "echo 'grep  example grep a abood using cat to display whats in file and nd in abood a and b the grep just show'",
        "more": "echo ' used when you have a large text file  and you want to read it in a more manageable way'",
        "ps": "echo 'ps aux displays detailed information about all running processes'",
        "rm": "echo 'rm file txt deletes the file named file txt'",
        "pwd": "echo 'pwd displays the full path of the current directory.'",
        "find": "echo 'find name txt finds all txt files in the current directory and its subdirectories'",
        "tail": "echo 'tail -n 5 filetxt displays the last 5 lines of filetxt'",
        "head": "echo 'head -n 5 filetxt displays the first 5 lines of filetxt'",
        "rmdir": "echo 'rmdir empty_folder deletes the directory named empty_folder if it's empty'",
        "echo": "echo ' prints Hello, World to the terminal'",
        "sudo": "echo 'sudo apt update runs the apt update command with root privileges'",
        
    }

    def __init__(self, command_name):
        self.command_name = command_name
        self.description = self._fetch_description()
        self.version_history = self._fetch_version_history()
        self.example = self.command_examples.get(command_name, "No example available.")
        self.related_commands = self._fetch_related_commands()
        self.syntax_usage = f"Syntax and usage patterns for {command_name}"
        self.documentation_links = [f"https://www.example.com/{command_name}-documentation"]
   
    def _fetch_description(self):
        try:
            man_command = f"man {self.command_name} | col -b"
            awk_command = f"awk '/^DESCRIPTION/{{flag=1; next}} /./{{if(flag)print}} /^$/{{if(flag)count++}} count==2{{flag=0}}'"
            
            man_output = subprocess.Popen(man_command, shell=True, stdout=subprocess.PIPE)
            awk_output = subprocess.Popen(awk_command, shell=True, stdin=man_output.stdout, stdout=subprocess.PIPE, text=True)
            
            man_output.stdout.close()
            final_output, _ = awk_output.communicate()

            return final_output.strip()
        except subprocess.CalledProcessError:
            return "documentation not found."
        pass
    def _fetch_version_history(self):
        try:
            version_output = subprocess.run([self.command_name, '--version'], capture_output=True, text=True).stdout
            return version_output.strip()
        except subprocess.CalledProcessError:
            return "not available."
        pass

    def _fetch_related_commands(self):
        try:
            related_command = f"bash -c 'compgen -c | grep ^{self.command_name} | head -5'"
            related_output = subprocess.run(related_command, shell=True, capture_output=True, text=True).stdout.strip().split('\n')
            return related_output
        except subprocess.CalledProcessError:
            return ["Error occurred while finding related commands."]
        




class XmlSerializer:
    def serialize(manual):
        manuals = ET.Element("Manuals")
        command_manual = ET.SubElement(manuals, "CommandManual")
        ET.SubElement(command_manual, "CommandName").text = manual.command_name
        ET.SubElement(command_manual, "CommandDescription").text = manual.description
        ET.SubElement(command_manual, "VersionHistory").text = manual.version_history
        ET.SubElement(command_manual, "Example").text = manual.example

        related_commands = ET.SubElement(command_manual, "RelatedCommands")
        for cmd in manual.related_commands:
            ET.SubElement(related_commands, "Command").text = cmd

        ET.SubElement(command_manual, "SyntaxAndUsage").text = manual.syntax_usage

        doc_links = ET.SubElement(command_manual, "DocumentationLinks")
        for link in manual.documentation_links:
            ET.SubElement(doc_links, "Link").text = link

        return XmlSerializer.prettify_xml(manuals)

    def prettify_xml(elem):
        rough_string = ET.tostring(elem, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")

class CommandManualGenerator:
    def __init__(self, commands):
        self.command_manuals = [CommandManual(command) for command in commands]

    def generate_manuals(self):
        xml_manuals = []
        for manual in self.command_manuals:
            try:
                xml_data = XmlSerializer.serialize(manual)
                xml_manuals.append(xml_data)
            except Exception as e:
                print(f"error serializing manual for command '{manual.command_name}': {e}")
        return xml_manuals
    
def view_commands():
    print("\nThe menu of commands available:")
    print("cat\ncp\ngrep\nls\nmkdir\nmv\nnano\npico\nsed\ntouch\nmore\ncd\nrm\npwd\nfind\ntail\nhead\nrmdir\necho\nsudo\n")



def search_available_commands():
    while True:
        command_name = input("\nEnter the command name to search (enter 0 to go back): ")
        if command_name == "0":
            break

        file_path = f"{command_name}.xml"
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                print(file.read())
        else:
            print(f"No matching command file found for {command_name}")

def recommend_command():
    home_directory = os.path.expanduser('~')
    history_file_path = os.path.join(home_directory, '.bash_history')
    
    try:
        with open(history_file_path, 'r') as history_file:
            history_commands = history_file.readlines()
        
        print("\nMost recently used commands:")
        for command in history_commands[-5:]:
            print(command.strip())
    except FileNotFoundError:
        print("\n.bash_history file not found.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")


def Verification():
    commands = read_commands_from_file("commands.txt")
    for command in commands:
        original_file = f"{command}.xml"
        copied_file = f"{command}1.xml"

        if os.path.exists(original_file) and os.path.exists(copied_file):
            with open(original_file, "r") as original, open(copied_file, "r") as copied:
                original_content = original.readlines()
                copied_content = copied.readlines()

                differ = difflib.Differ()
                diff = list(differ.compare(original_content, copied_content))

                differences = [line for line in diff if line.startswith('-') or line.startswith('+')]
                if not differences:
                    print(f"no differences found for command '{command}'.")
                else:
                    print(f"Differences found for command '{command}':")
                    for line in differences:
                        print("the differences is:" ,line.strip())
        else:
            print(f"file missing for command '{command}'")


def read_commands_from_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines() if line.strip()]


def main():


    while True:
        print("\nYour choice:")
        print("1. view commands available")
        print("2. create command files for the available commands")
        print("3. search available command files to display them")
        print("4. verification")
        print("5. recommend command")
        print("6. exit the program\n")

        choice = input("Please enter a number between 1-6: ")

        if choice == '1':
            view_commands()
        elif choice == '2':
         try:
                commands = read_commands_from_file("commands.txt")
                generator = CommandManualGenerator(commands)
                xml_manuals = generator.generate_manuals()
                for manual, command in zip(xml_manuals, commands):
                     file_name = f"{command}.xml"
                     with open(file_name, "w") as file:
                        file.write(manual)
                     copied_file_name = f"{command}1.xml"
                     shutil.copy(file_name, copied_file_name)
                     print(f"create {command}.xml done ")
         except FileNotFoundError:
                print("error: 'commands.txt' file not found.")
        
        elif choice == '3':
            search_available_commands()
        elif choice == '4':
            Verification()
        elif choice == '5':
            recommend_command()
        elif choice == '6':
            print("\nbye thank you for using my porgram")
            break
        else:
            print("incorrect choice please enter number between [1-6].")

if __name__ == "__main__":
    main()