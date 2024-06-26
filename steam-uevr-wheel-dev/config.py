from cx_Freeze import setup, Executable

setup(
    name="steam-uevr-wheel",
    version="0.1",
    description="My Application",
    executables=[Executable("open-vr-wheel.py", icon="steam-uevr-wheel.ico")]
)
