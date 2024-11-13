import platform
import subprocess
import os
import sys

def main():
    if platform.system() == 'Windows':
        # Lansăm Notepad și așteptăm să se închidă
        process = subprocess.Popen(['notepad', 'test.txt'])
        exit_code = process.wait()
        print(f"Editorul s-a închis cu codul de terminare {exit_code}")

        # Creăm un fișier batch în folderul Startup pentru a deschide fișierul după restart
        startup_folder = os.path.join(os.environ["APPDATA"], "Microsoft\\Windows\\Start Menu\\Programs\\Startup")
        batch_file_path = os.path.join(startup_folder, 'open_test_file.bat')
        with open(batch_file_path, 'w') as batch_file:
            batch_file.write(f'@echo off\nstart notepad.exe "{os.path.abspath("test.txt")}"\ndel "%~f0"\n')

        # Repornim sistemul
        print("Sistemul va fi repornit în câteva secunde...")
        os.system('shutdown /r /t 5')

    elif platform.system() == 'Linux':
        # Lansăm Gedit și așteptăm să se închidă
        process = subprocess.Popen(['gedit', 'test.txt'])
        exit_code = process.wait()
        print(f"Editorul s-a închis cu codul de terminare {exit_code}")

        # Creăm un fișier .desktop în folderul autostart pentru a deschide fișierul după restart
        autostart_dir = os.path.expanduser('~/.config/autostart')
        if not os.path.exists(autostart_dir):
            os.makedirs(autostart_dir)

        desktop_file_path = os.path.join(autostart_dir, 'open_test_file.desktop')

        desktop_entry = f"""[Desktop Entry]
Type=Application
Exec=sh -c 'gedit "{os.path.abspath('test.txt')}" ; rm -f "{os.path.abspath(desktop_file_path)}"'
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Name=Open Test File
Comment=Deschide fișierul test.txt după restart
"""

        with open(desktop_file_path, 'w') as desktop_file:
            desktop_file.write(desktop_entry)

        # Verificăm dacă scriptul este rulat cu drepturi de administrator
        if os.geteuid() != 0:
            print("Vă rugăm să rulați acest script cu drepturi de administrator (sudo).")
            sys.exit(1)

        # Repornim sistemul
        print("Sistemul va fi repornit în câteva secunde...")
        os.system('shutdown -r now')
    else:
        print("Sistem de operare nesuportat.")

if __name__ == "__main__":
    main()
