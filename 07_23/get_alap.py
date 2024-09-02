import os

def screener():
    options = ["Python [py]", "C [c]", "quit"]
    
    print("----------------------------")
    print('Create an empty source file')
    print("----------------------------")
    
    for i, option in enumerate(options):
        print(f"{i + 1}. {option}")
        
    my_choice = int(input("> "))
    
    if my_choice not in [1, 2, 3]:
        print("Invalid choice")
        return None

    return my_choice

def create_py_file():
    with open("alap.py", "w") as f:
        f.write("# Path: 07_23/alap.py\n")
        f.write("def main():\n")
        f.write("    print('Hello, World!')\n")
        f.write("\n")
        f.write("if __name__ == '__main__':\n")
        f.write("    main()\n")
    
    print("File created: alap.py")
    
def create_c_file():
    with open("alap.c", "w") as f:
        f.write("/* Path: 07_23/alap.c */\n")
        f.write("#include <stdio.h>\n")
        f.write("\n")
        f.write("int main() {\n")
        f.write("    printf(\"Hello, World!\\n\");\n")
        f.write("    return 0;\n")
        f.write("}\n")
    
    print("File created: alap.c")
    
def quit():
    print("Goodbye!")

def main():
    while True:
        try:
            choice = screener()
        except ValueError:
            print("Please enter a number in the range 1-3")
            continue
        if choice == 1:
            if os.path.isfile("alap.py"):
                print("File already exists: alap.py")
                continue
            create_py_file()
        elif choice == 2:
            if os.path.isfile("alap.c"):
                print("File already exists: alap.c")
                continue
            create_c_file()
        elif choice == 3:
            quit()
            break        
    
if __name__ == '__main__':
    main()