FF MAX BOOSTER — Windows build package
=======================================

What it does
------------
- Detects basic Windows laptop information (CPU, logical cores, RAM, graphics name).
- Suggests a conservative BlueStacks 5 64-bit starting profile based mainly on RAM.
- Provides shortcuts to BlueStacks settings and Windows power settings.
- Does NOT modify game files, emulator configuration files, anti-cheat, drivers, registry,
  or hardware clocks.

Build the EXE
-------------
1. Install Python 3.10 or newer on Windows from python.org.
2. During installation, enable "Add Python to PATH".
3. Extract this folder.
4. Double-click build_exe.bat.
5. The finished application will be:
   dist\FF_MAX_Booster.exe

The EXE is built on your own Windows laptop. This package contains the source and build
script; it is not itself a precompiled Windows executable.

Important FPS limitations
-------------------------
A 60 Hz display can show up to 60 distinct frames per second. 120–144 FPS requires
a compatible high-refresh display and support from the game, BlueStacks, GPU and drivers.
No utility can guarantee a fixed FPS across all laptop models.

Suggested starting points
-------------------------
4 GB RAM: 2 cores / 1.5 GB RAM / 960x540; close background apps.
8 GB RAM: 2 cores / 3 GB RAM / 1280x720.
16 GB RAM: 4 cores / 4–6 GB RAM / 1280x720.
32 GB RAM: 4 cores / 6–8 GB RAM / choose resolution based on GPU.

These are starting points, not universal optimum settings. If Windows stutters, lower
the emulator RAM allocation or close other applications.
