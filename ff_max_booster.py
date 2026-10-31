import os
import platform
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox

APP_NAME = "FF MAX Booster"

def run_powershell(command):
    try:
        return subprocess.check_output(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", command],
            text=True, stderr=subprocess.DEVNULL, timeout=8
        ).strip()
    except Exception:
        return ""

def get_specs():
    cpu = platform.processor() or "Not reported by Windows"
    cores = os.cpu_count() or 2
    total_ram_gb = 0
    try:
        import ctypes
        class MEMORYSTATUSEX(ctypes.Structure):
            _fields_ = [
                ("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong),
                ("ullTotalPhys", ctypes.c_ulonglong), ("ullAvailPhys", ctypes.c_ulonglong),
                ("ullTotalPageFile", ctypes.c_ulonglong), ("ullAvailPageFile", ctypes.c_ulonglong),
                ("ullTotalVirtual", ctypes.c_ulonglong), ("ullAvailVirtual", ctypes.c_ulonglong),
                ("ullAvailExtendedVirtual", ctypes.c_ulonglong)
            ]
        stat = MEMORYSTATUSEX()
        stat.dwLength = ctypes.sizeof(stat)
        if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat)):
            total_ram_gb = round(stat.ullTotalPhys / (1024**3))
    except Exception:
        pass
    gpu = run_powershell(
        "Get-CimInstance Win32_VideoController | "
        "Select-Object -ExpandProperty Name | Out-String"
    )
    display = run_powershell(
        "Get-CimInstance Win32_VideoController | "
        "Select-Object -ExpandProperty CurrentRefreshRate | Out-String"
    )
    return cpu, cores, total_ram_gb, gpu or "Not detected", display or "Not detected"

def recommendations(ram, cores):
    if ram <= 4:
        return ("2 cores", "1536 MB", "960 x 540", "30–45 FPS target",
                "Close other apps; 8 GB RAM is strongly recommended for smoother emulation.")
    if ram <= 8:
        return ("2 cores", "3072 MB", "1280 x 720", "60 FPS target",
                "Keep background apps closed. Do not allocate all system RAM to BlueStacks.")
    if ram <= 16:
        return ("4 cores" if cores >= 4 else "2 cores", "4096–6144 MB",
                "1280 x 720", "60 FPS; higher only if supported",
                "Use the lower RAM allocation if Windows becomes unresponsive.")
    return ("4 cores" if cores >= 4 else "2 cores", "6144–8192 MB",
            "1920 x 1080 or 1280 x 720", "60 FPS; higher only if supported",
            "Choose resolution based on GPU load and laptop temperature.")

class Booster(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_NAME)
        self.geometry("720x650")
        self.minsize(650, 600)
        self.configure(bg="#101722")
        self.cpu, self.cores, self.ram, self.gpu, self.refresh = get_specs()
        self.build()

    def build(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#101722")
        style.configure("TLabel", background="#101722", foreground="#edf2f7", font=("Segoe UI", 10))
        style.configure("Header.TLabel", font=("Segoe UI", 22, "bold"), foreground="#66d9ef")
        style.configure("Sub.TLabel", foreground="#aab7c4")
        style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=9)
        outer = ttk.Frame(self, padding=22)
        outer.pack(fill="both", expand=True)
        ttk.Label(outer, text="FF MAX BOOSTER", style="Header.TLabel").pack(anchor="w")
        ttk.Label(outer, text="BlueStacks 5 • 64-bit • Windows laptop helper", style="Sub.TLabel").pack(anchor="w", pady=(2, 16))

        specs = (
            f"Processor: {self.cpu}\nCPU logical cores: {self.cores}\n"
            f"Installed RAM: {self.ram or 'Unknown'} GB\nGraphics: {self.gpu.strip()}\n"
            f"Reported display refresh: {self.refresh.strip()}"
        )
        self.card(outer, "DETECTED LAPTOP", specs)

        cpu, mem, res, fps, note = recommendations(self.ram or 8, self.cores)
        rec = (f"BlueStacks CPU: {cpu}\nBlueStacks RAM: {mem}\nResolution: {res}\n"
               f"Initial FPS target: {fps}\n\n{note}")
        self.card(outer, "SUGGESTED STARTING PROFILE", rec)

        ttk.Label(outer, text="QUICK ACTIONS", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(14, 8))
        buttons = ttk.Frame(outer)
        buttons.pack(fill="x")
        ttk.Button(buttons, text="Open BlueStacks Settings", command=self.open_settings).pack(side="left", padx=(0, 8))
        ttk.Button(buttons, text="Open Windows Power Settings", command=self.open_power).pack(side="left", padx=8)
        ttk.Button(buttons, text="Refresh Detection", command=self.refresh_specs).pack(side="left", padx=8)

        warning = ("FPS note: a 60 Hz screen can display up to 60 distinct frames per second. "
                   "120–144 FPS is not guaranteed and depends on the laptop display, GPU, "
                   "game support, emulator version and thermal limits. This tool does not "
                   "modify Free Fire MAX files, bypass anti-cheat, overclock hardware, or "
                   "promise extra FPS.")
        ttk.Label(outer, text=warning, wraplength=660, style="Sub.TLabel").pack(anchor="w", pady=(18, 0))

    def card(self, parent, title, body):
        frame = tk.Frame(parent, bg="#1b2938", padx=14, pady=12)
        frame.pack(fill="x", pady=6)
        tk.Label(frame, text=title, bg="#1b2938", fg="#66d9ef",
                 font=("Segoe UI", 10, "bold")).pack(anchor="w")
        tk.Label(frame, text=body, bg="#1b2938", fg="#edf2f7",
                 justify="left", anchor="w", font=("Segoe UI", 10),
                 wraplength=650).pack(anchor="w", pady=(7, 0))

    def open_settings(self):
        candidates = [
            os.path.join(os.environ.get("ProgramFiles", r"C:\Program Files"),
                         "BlueStacks_nxt", "HD-Player.exe"),
            os.path.join(os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)"),
                         "BlueStacks_nxt", "HD-Player.exe")
        ]
        found = next((p for p in candidates if os.path.exists(p)), None)
        if found:
            try:
                subprocess.Popen([found, "--settings"])
                return
            except Exception:
                pass
        messagebox.showinfo("BlueStacks", "Open BlueStacks 5 manually, then choose Settings (gear icon).")

    def open_power(self):
        try:
            subprocess.Popen(["control.exe", "powercfg.cpl"])
        except Exception:
            messagebox.showinfo("Power settings", "Open Windows Settings > System > Power & battery.")

    def refresh_specs(self):
        self.destroy()
        Booster().mainloop()

if __name__ == "__main__":
    Booster().mainloop()
