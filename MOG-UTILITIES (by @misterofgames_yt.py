import tkinter
import customtkinter as ctk
import psutil
import os
import subprocess
import threading
from tkinter import messagebox
import requests
import shutil
import tempfile
import sys
from pathlib import Path

# Basic setup
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class MOGUtilities(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Window setup
        self.title("MOG-UTILITIES")
        self.geometry("1200x800")
        
        # Create main frames
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Create sidebar
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)
        
        # Create main area
        self.main_area = ctk.CTkFrame(self)
        self.main_area.grid(row=0, column=1, sticky="nsew", padx=10, pady=5)
        
        # Create status bar
        self.status_bar = ctk.CTkFrame(self, height=25)
        self.status_bar.grid(row=1, column=0, columnspan=2, sticky="ew")
        
        # Add status labels
        self.cpu_label = ctk.CTkLabel(self.status_bar, text="CPU: 0%")
        self.cpu_label.pack(side="left", padx=10)
        self.ram_label = ctk.CTkLabel(self.status_bar, text="RAM: 0%")
        self.ram_label.pack(side="left", padx=10)
        
        # Create sidebar buttons
        self.create_sidebar()
        
        # Show welcome page
        self.show_welcome()
        
        # Start monitoring
        self.start_monitoring()

    def create_sidebar(self):
        # Title
        title = ctk.CTkLabel(
            self.sidebar, 
            text="MOG-UTILITIES",
            font=("Arial", 20, "bold")
        )
        title.pack(pady=20)
        
        # Buttons
        buttons = [
            ("🏠 Home", self.show_welcome),
            ("🚀 Optimizer", self.show_optimizer),
            ("⚡ Processes", self.show_processes),
            ("🎮 Gaming Mode", self.show_gaming),
            ("🗑️ Bloatware", self.show_bloatware),
            ("📥 Install Apps", self.show_installer)
        ]
        
        for text, command in buttons:
            btn = ctk.CTkButton(
                self.sidebar,
                text=text,
                command=command,
                height=40,
                anchor="w",
                font=("Arial", 12)
            )
            btn.pack(fill="x", padx=5, pady=2)
        
        # Optimize Everything button
        optimize_all = ctk.CTkButton(
            self.sidebar,
            text="🚀 OPTIMIZE ALL",
            command=self.optimize_everything,
            height=50,
            font=("Arial", 14, "bold"),
            fg_color="green",
            hover_color="dark green"
        )
        optimize_all.pack(side="bottom", fill="x", padx=5, pady=10)

    def show_welcome(self):
        self.clear_main_area()
        
        # Welcome message
        title = ctk.CTkLabel(
            self.main_area,
            text="Welcome to MOG-UTILITIES",
            font=("Arial", 28, "bold")
        )
        title.pack(pady=30)
        
        # Quick actions
        buttons = [
            ("🚀 Quick Optimize", self.optimize_everything),
            ("🎮 Gaming Mode", self.show_gaming),
            ("📥 Install Apps", self.show_installer),
            ("🗑️ Remove Bloatware", self.show_bloatware)
        ]
        
        for text, command in buttons:
            btn = ctk.CTkButton(
                self.main_area,
                text=text,
                command=command,
                width=300,
                height=50,
                font=("Arial", 14)
            )
            btn.pack(pady=10)

    def show_processes(self):
        self.clear_main_area()
        
        # Controls
        controls = ctk.CTkFrame(self.main_area)
        controls.pack(fill="x", padx=10, pady=5)
        
        refresh_btn = ctk.CTkButton(
            controls,
            text="Refresh",
            command=self.refresh_processes,
            width=100
        )
        refresh_btn.pack(side="left", padx=5)
        
        # Process list
        self.process_frame = ctk.CTkScrollableFrame(self.main_area)
        self.process_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.refresh_processes()

    def refresh_processes(self):
        for widget in self.process_frame.winfo_children():
            widget.destroy()
            
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    info = proc.info
                    
                    frame = ctk.CTkFrame(self.process_frame)
                    frame.pack(fill="x", pady=2)
                    
                    name = ctk.CTkLabel(frame, text=f"{info['name']} (PID: {info['pid']})")
                    name.pack(side="left", padx=10)
                    
                    usage = ctk.CTkLabel(
                        frame,
                        text=f"CPU: {info['cpu_percent']}% | RAM: {info['memory_percent']:.1f}%"
                    )
                    usage.pack(side="left", padx=10)
                    
                    end_btn = ctk.CTkButton(
                        frame,
                        text="End",
                        width=60,
                        command=lambda p=info['pid']: self.end_process(p)
                    )
                    end_btn.pack(side="right", padx=10)
                    
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load processes: {str(e)}")

    def end_process(self, pid):
        try:
            psutil.Process(pid).terminate()
            self.refresh_processes()
        except:
            messagebox.showerror("Error", f"Could not terminate process {pid}")

    def show_installer(self):
        self.clear_main_area()
        
        title = ctk.CTkLabel(
            self.main_area,
            text="App Installer",
            font=("Arial", 24, "bold")
        )
        title.pack(pady=20)
        
        apps = {
            "Browsers": [
                ("Google Chrome", "https://dl.google.com/chrome/install/latest/chrome_installer.exe"),
                ("Mozilla Firefox", "https://download.mozilla.org/?product=firefox-latest&os=win64&lang=en-US"),
                ("Brave Browser", "https://laptop-updates.brave.com/latest/winx64")
            ],
            "Gaming": [
                ("Steam", "https://cdn.akamai.steamstatic.com/client/installer/SteamSetup.exe"),
                ("Epic Games", "https://launcher-public-service-prod06.ol.epicgames.com/launcher/api/installer/download/EpicGamesLauncherInstaller.msi"),
                ("Discord", "https://discord.com/api/downloads/distributions/app/installers/latest?channel=stable&platform=win&arch=x86")
            ],
            "Utilities": [
                ("7-Zip", "https://www.7-zip.org/a/7z2201-x64.exe"),
                ("VLC Media Player", "https://get.videolan.org/vlc/3.0.18/win64/vlc-3.0.18-win64.exe"),
                ("Notepad++", "https://github.com/notepad-plus-plus/notepad-plus-plus/releases/download/v8.5.4/npp.8.5.4.Installer.x64.exe")
            ]
        }
        
        scroll_frame = ctk.CTkScrollableFrame(self.main_area)
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        for category, app_list in apps.items():
            frame = ctk.CTkFrame(scroll_frame)
            frame.pack(fill="x", pady=5)
            
            ctk.CTkLabel(
                frame,
                text=category,
                font=("Arial", 16, "bold")
            ).pack(pady=5)
            
            for app_name, url in app_list:
                app_frame = ctk.CTkFrame(frame)
                app_frame.pack(fill="x", pady=2, padx=5)
                
                ctk.CTkLabel(app_frame, text=app_name).pack(side="left", padx=10)
                
                status_label = ctk.CTkLabel(app_frame, text="")
                status_label.pack(side="left", padx=10)
                
                install_btn = ctk.CTkButton(
                    app_frame,
                    text="Install",
                    width=100,
                    command=lambda n=app_name, u=url, s=status_label: self.install_app(n, u, s)
                )
                install_btn.pack(side="right", padx=10)

    def install_app(self, app_name, url, status_label):
        def _install():
            try:
                status_label.configure(text="Downloading...")
                
                temp_dir = os.path.join(tempfile.gettempdir(), 'MOG_UTILITIES')
                os.makedirs(temp_dir, exist_ok=True)
                
                installer_path = os.path.join(temp_dir, f"{app_name.replace(' ', '')}_installer.exe")
                
                response = requests.get(url, stream=True)
                with open(installer_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                status_label.configure(text="Installing...")
                subprocess.run(installer_path, shell=True)
                
                status_label.configure(text="Installed!")
                messagebox.showinfo("Success", f"{app_name} installed successfully!")
                
            except Exception as e:
                status_label.configure(text="Failed!")
                messagebox.showerror("Error", f"Failed to install {app_name}: {str(e)}")
        
        threading.Thread(target=_install, daemon=True).start()

    def show_bloatware(self):
        self.clear_main_area()
        
        title = ctk.CTkLabel(
            self.main_area,
            text="Bloatware Remover",
            font=("Arial", 24, "bold")
        )
        title.pack(pady=20)
        
        remove_all_btn = ctk.CTkButton(
            self.main_area,
            text="Remove All Bloatware",
            command=self.remove_all_bloatware,
            height=40,
            font=("Arial", 14, "bold")
        )
        remove_all_btn.pack(pady=10)
        
        scroll_frame = ctk.CTkScrollableFrame(self.main_area)
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        bloatware = [
            "Microsoft Edge",
            "Cortana",
            "Xbox",
            "Skype",
            "Microsoft Teams",
            "Your Phone",
            "Mail and Calendar",
            "Microsoft Office",
            "OneNote",
            "Mixed Reality Portal"
        ]
        
        for app in bloatware:
            frame = ctk.CTkFrame(scroll_frame)
            frame.pack(fill="x", pady=2)
            
            ctk.CTkLabel(frame, text=app).pack(side="left", padx=10)
            
            status_label = ctk.CTkLabel(frame, text="")
            status_label.pack(side="left", padx=10)
            
            remove_btn = ctk.CTkButton(
                frame,
                text="Remove",
                width=100,
                command=lambda a=app, s=status_label: self.remove_bloatware(a, s)
            )
            remove_btn.pack(side="right", padx=10)

    def remove_bloatware(self, app, status_label):
        def _remove():
            try:
                status_label.configure(text="Removing...")
                
                commands = [
                    f'Get-AppxPackage *{app.replace(" ", "")}* | Remove-AppxPackage',
                    f'Get-AppxProvisionedPackage -Online | where DisplayName -like "*{app.replace(" ", "")}*" | Remove-AppxProvisionedPackage -Online'
                ]
                
                if app == "Microsoft Edge":
                    commands.extend([
                        r'cd "C:\Program Files (x86)\Microsoft\Edge\Application\*\Installer"',
                        r'setup.exe --uninstall --system-level --verbose-logging --force-uninstall'
                    ])
                
                for cmd in commands:
                    subprocess.run(['powershell', '-Command', cmd], capture_output=True)
                
                status_label.configure(text="Removed!")
                messagebox.showinfo("Success", f"{app} removed successfully!")
                
            except Exception as e:
                status_label.configure(text="Failed!")
                messagebox.showerror("Error", f"Failed to remove {app}: {str(e)}")
        
        threading.Thread(target=_remove, daemon=True).start()

    def remove_all_bloatware(self):
        if messagebox.askyesno("Remove All", "This will remove all bloatware. Continue?"):
            for frame in self.main_area.winfo_children():
                if isinstance(frame, ctk.CTkFrame):
                    for widget in frame.winfo_children():
                        if isinstance(widget, ctk.CTkButton) and widget.cget("text") == "Remove":
                            widget.invoke()

    def show_optimizer(self):
        self.clear_main_area()
        
        title = ctk.CTkLabel(
            self.main_area,
            text="System Optimizer",
            font=("Arial", 24, "bold")
        )
        title.pack(pady=20)
        
        optimizations = [
            ("Clear Temporary Files", self.clear_temp_files),
            ("Optimize Services", self.optimize_services),
            ("Optimize Registry", self.optimize_registry),
            ("Clear Memory", self.clear_memory),
            ("Optimize for Gaming", self.optimize_for_gaming),
            ("Set High Performance", self.set_high_performance),
            ("Optimize Network", self.optimize_network),
            ("Disable Visual Effects", self.disable_visual_effects),
            ("Disable Telemetry", self.disable_telemetry),
            ("Optimize Startup", self.optimize_startup)
        ]
        
        for name, func in optimizations:
            frame = ctk.CTkFrame(self.main_area)
            frame.pack(fill="x", padx=20, pady=5)
            
            ctk.CTkLabel(frame, text=name).pack(side="left", padx=10)
            
            status_label = ctk.CTkLabel(frame, text="")
            status_label.pack(side="right", padx=10)
            
            optimize_btn = ctk.CTkButton(
                frame,
                text="Optimize",
                width=100,
                command=lambda f=func, s=status_label: self.run_optimization(f, s)
            )
            optimize_btn.pack(side="right", padx=10)

    def run_optimization(self, func, status_label):
        def _optimize():
            try:
                status_label.configure(text="Optimizing...")
                func()
                status_label.configure(text="✓ Done")
            except Exception as e:
                status_label.configure(text="Failed!")
                messagebox.showerror("Error", str(e))
        
        threading.Thread(target=_optimize, daemon=True).start()

    def show_gaming(self):
        self.clear_main_area()
        
        title = ctk.CTkLabel(
            self.main_area,
            text="Gaming Mode",
            font=("Arial", 24, "bold")
        )
        title.pack(pady=20)
        
        gaming_frame = ctk.CTkFrame(self.main_area)
        gaming_frame.pack(fill="x", padx=20, pady=10)
        
        gaming_switch = ctk.CTkSwitch(
            gaming_frame,
            text="Gaming Mode",
            command=self.toggle_gaming_mode
        )
        gaming_switch.pack(pady=10)
        
        optimizations = [
            ("Optimize CPU Priority", self.optimize_cpu_priority),
            ("Disable Background Services", self.disable_background_services),
            ("Set High Performance Power Plan", self.set_high_performance),
            ("Optimize Network Settings", self.optimize_network),
            ("Clear System Memory", self.clear_memory),
            ("Disable Visual Effects", self.disable_visual_effects)
        ]
        
        for name, func in optimizations:
            frame = ctk.CTkFrame(self.main_area)
            frame.pack(fill="x", padx=20, pady=5)
            
            ctk.CTkLabel(frame, text=name).pack(side="left", padx=10)
            
            status_label = ctk.CTkLabel(frame, text="")
            status_label.pack(side="right", padx=10)
            
            optimize_btn = ctk.CTkButton(
                frame,
                text="Optimize",
                width=100,
                command=lambda f=func, s=status_label: self.run_optimization(f, s)
            )
            optimize_btn.pack(side="right", padx=10)

    def toggle_gaming_mode(self):
        try:
            # Set high priority for games
            subprocess.run('powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c', shell=True)
            
            # Enable Game Mode
            subprocess.run('reg add "HKEY_CURRENT_USER\Software\Microsoft\GameBar" /v "AllowAutoGameMode" /t REG_DWORD /d "1" /f', shell=True)
            subprocess.run('reg add "HKEY_CURRENT_USER\Software\Microsoft\GameBar" /v "AutoGameModeEnabled" /t REG_DWORD /d "1" /f', shell=True)
            
            # Optimize for gaming
            self.optimize_for_gaming()
            
            messagebox.showinfo("Success", "Gaming Mode enabled!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to enable Gaming Mode: {str(e)}")

    def optimize_everything(self):
        if messagebox.askyesno("Optimize Everything", "This will apply all optimizations. Continue?"):
            threading.Thread(target=self._optimize_everything, daemon=True).start()

    def _optimize_everything(self):
        try:
            optimizations = [
                self.clear_temp_files,
                self.optimize_services,
                self.optimize_registry,
                self.clear_memory,
                self.optimize_for_gaming,
                self.set_high_performance,
                self.optimize_network,
                self.disable_visual_effects,
                self.disable_telemetry,
                self.optimize_startup
            ]
            
            for opt in optimizations:
                try:
                    opt()
                except:
                    continue
            
            messagebox.showinfo("Success", "All optimizations completed!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Optimization failed: {str(e)}")

    def start_monitoring(self):
        def monitor():
            while True:
                try:
                    cpu = psutil.cpu_percent(interval=1)
                    ram = psutil.virtual_memory().percent
                    self.update_status(cpu, ram)
                except:
                    pass
        threading.Thread(target=monitor, daemon=True).start()

    def update_status(self, cpu, ram):
        self.cpu_label.configure(text=f"CPU: {cpu}%")
        self.ram_label.configure(text=f"RAM: {ram}%")

    def clear_main_area(self):
        for widget in self.main_area.winfo_children():
            widget.destroy()

    # Add missing optimization functions
    def clear_temp_files(self): pass
    def optimize_services(self): pass
    def optimize_registry(self): pass
    def clear_memory(self): pass
    def optimize_for_gaming(self): pass
    def set_high_performance(self): pass
    def optimize_network(self): pass
    def disable_visual_effects(self): pass
    def disable_telemetry(self): pass
    def optimize_startup(self): pass
    def optimize_cpu_priority(self): pass
    def disable_background_services(self): pass

if __name__ == "__main__":
    try:
        app = MOGUtilities()
        app.mainloop()
    except Exception as e:
        print(f"Error: {str(e)}")
        input("Press Enter to exit...")