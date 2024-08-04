import sys
from cx_Freeze import setup, Executable

# Include additional packages or modules if needed
build_exe_options = {
    "packages": [],  # Add any additional packages here
    "excludes": []
}

base = None

# Define the Executable and provide the icon file
executables = [
    Executable(
        script="open-vr-wheel.py",  # Your main Python script
        base=base,
        icon="steam-uevr-wheel.ico"  # Path to your custom icon file
    )
]

setup(
    name="steam-uevr-wheel",
    version="0.1",
    description="A simple steering wheel overlay mechanism for VR",
    options={"build_exe": build_exe_options},
    executables=executables
)
