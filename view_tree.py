# HΛRM TOOL: view_tree.py
# PURPOSE: View the current ΞΣ_TREE_VIEW.txt in the terminal

def display_tree():
    try:
        with open("ΞΣ_TREE_VIEW.txt", "r", encoding="utf-8") as tree:
            print(tree.read())
    except FileNotFoundError:
        print("ΞΣ_TREE_VIEW.txt not found. No recursion tree has been recorded yet.")

if __name__ == "__main__":
    display_tree()
