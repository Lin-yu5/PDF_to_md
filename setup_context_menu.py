"""
Windows Explorer Context Menu Setup for PDF to Markdown Converter.
Adds or removes a right-click 'Convert to Markdown (.md)' entry for .pdf files.
Registers under HKEY_CURRENT_USER so no administrator privileges are required.
Also generates portable .reg files for direct registry import.
"""

import sys
import os
import argparse
import winreg

REG_SUBKEY = r"Software\Classes\SystemFileAssociations\.pdf\shell\ConvertToMarkdown"
DEFAULT_MENU_NAME = "Convert to Markdown (.md)"


def get_paths():
    """Detect pythonw.exe and pdf_to_md.py paths."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    target_script = os.path.join(script_dir, "pdf_to_md.py")

    if not os.path.exists(target_script):
        raise FileNotFoundError(f"Target script not found: {target_script}")

    # Look for pythonw.exe in python directory to run silently without popping up cmd window
    python_dir = os.path.dirname(sys.executable)
    pythonw = os.path.join(python_dir, "pythonw.exe")
    if not os.path.exists(pythonw):
        pythonw = sys.executable

    return pythonw, target_script


def generate_reg_files(pythonw: str, target_script: str, menu_name: str = DEFAULT_MENU_NAME):
    """Generate portable .reg files configured with current system paths."""
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Escape backslashes for .reg file format
    esc_pythonw = pythonw.replace("\\", "\\\\")
    esc_script = target_script.replace("\\", "\\\\")

    # Registration .reg content
    add_reg_content = (
        "Windows Registry Editor Version 5.00\r\n\r\n"
        "[HKEY_CURRENT_USER\\Software\\Classes\\SystemFileAssociations\\.pdf\\shell\\ConvertToMarkdown]\r\n"
        f'@="{menu_name}"\r\n'
        f'"Icon"="notepad.exe"\r\n\r\n'
        "[HKEY_CURRENT_USER\\Software\\Classes\\SystemFileAssociations\\.pdf\\shell\\ConvertToMarkdown\\command]\r\n"
        f'@="\\"{esc_pythonw}\\" \\"{esc_script}\\" \\"%1\\""\r\n'
    )

    # Removal .reg content
    remove_reg_content = (
        "Windows Registry Editor Version 5.00\r\n\r\n"
        "[-HKEY_CURRENT_USER\\Software\\Classes\\SystemFileAssociations\\.pdf\\shell\\ConvertToMarkdown]\r\n"
    )

    add_reg_path = os.path.join(script_dir, "add_pdf_to_md_context.reg")
    remove_reg_path = os.path.join(script_dir, "remove_pdf_to_md_context.reg")

    with open(add_reg_path, "w", encoding="utf-8") as f:
        f.write(add_reg_content)

    with open(remove_reg_path, "w", encoding="utf-8") as f:
        f.write(remove_reg_content)

    return add_reg_path, remove_reg_path


def install_context_menu(menu_name: str = DEFAULT_MENU_NAME):
    """Register context menu in HKCU or generate reg file."""
    pythonw, target_script = get_paths()
    command_str = f'"{pythonw}" "{target_script}" "%1"'

    print("[*] Configuring Windows right-click context menu...")
    print(f"    - Target Script : {target_script}")
    print(f"    - Python Exec   : {pythonw}")
    print(f"    - Command       : {command_str}")

    # Generate / update .reg files
    add_reg, _ = generate_reg_files(pythonw, target_script, menu_name)
    print(f"    - Generated     : {add_reg}")

    # Try direct registry modification
    try:
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, REG_SUBKEY) as key:
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, menu_name)
            winreg.SetValueEx(key, "Icon", 0, winreg.REG_SZ, pythonw)

        cmd_subkey = fr"{REG_SUBKEY}\command"
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, cmd_subkey) as cmd_key:
            winreg.SetValueEx(cmd_key, "", 0, winreg.REG_SZ, command_str)

        print("\n[+] Successfully registered context menu directly to registry!")
        print(f"    Right-click any .pdf file in File Explorer to see '{menu_name}'.")
        return True
    except Exception as e:
        print(f"\n[!] Direct registry write encountered: {e}")
        print("[*] Attempting registration via reg import...")
        import subprocess
        res = subprocess.run(["reg", "import", add_reg], capture_output=True, text=True)
        if res.returncode == 0:
            print("[+] Successfully registered context menu via reg import!")
            return True
        else:
            print(f"[!] Please double-click '{os.path.basename(add_reg)}' to apply context menu.")
            return False


def delete_key_recursively(root_key, subkey):
    """Recursively delete a registry key and all subkeys."""
    try:
        with winreg.OpenKey(root_key, subkey, 0, winreg.KEY_ALL_ACCESS) as key:
            while True:
                try:
                    sub = winreg.EnumKey(key, 0)
                    delete_key_recursively(root_key, f"{subkey}\\{sub}")
                except OSError:
                    break
        winreg.DeleteKey(root_key, subkey)
    except FileNotFoundError:
        pass


def uninstall_context_menu():
    """Remove context menu registration from HKCU."""
    print("[*] Removing Windows right-click context menu...")
    _, remove_reg = generate_reg_files(*get_paths())
    try:
        delete_key_recursively(winreg.HKEY_CURRENT_USER, REG_SUBKEY)
        print("[+] Successfully removed context menu.")
        return True
    except Exception as e:
        print(f"[!] Direct removal encountered: {e}")
        print("[*] Attempting removal via reg import...")
        import subprocess
        res = subprocess.run(["reg", "import", remove_reg], capture_output=True, text=True)
        if res.returncode == 0:
            print("[+] Successfully removed context menu via reg import.")
            return True
        else:
            print(f"[!] Please double-click '{os.path.basename(remove_reg)}' to remove registry entry.")
            return False


def main():
    parser = argparse.ArgumentParser(
        description="Install or remove Windows right-click context menu for PDF-to-Markdown conversion."
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--install",
        action="store_true",
        help="Install context menu (default)",
    )
    group.add_argument(
        "--uninstall",
        "--remove",
        action="store_true",
        help="Remove context menu",
    )
    parser.add_argument(
        "--menu-name",
        type=str,
        default=DEFAULT_MENU_NAME,
        help=f"Custom display text for context menu (default: '{DEFAULT_MENU_NAME}')",
    )

    args = parser.parse_args()

    if args.uninstall:
        uninstall_context_menu()
    else:
        install_context_menu(args.menu_name)


if __name__ == "__main__":
    main()
