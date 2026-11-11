import os
import sys
import glob
from SCons.Script import Import

Import("env")

# Keep a caller-supplied path. Do not sys.exit: this runs inside PlatformIO.
if "OPENOCD_BIN" not in os.environ:
    openocd_bin = "openocd"
    if sys.platform == "darwin":
        pattern = "/Applications/STM32CubeIDE.app/Contents/Eclipse/plugins/com.st.stm32cube.ide.mcu.externaltools.openocd.*/tools/bin/openocd"
    elif sys.platform == "win32":
        pattern = r"C:\ST\STM32CubeIDE*\STM32CubeIDE\plugins\com.st.stm32cube.ide.mcu.externaltools.openocd.*\tools\bin\openocd.exe"
    elif sys.platform.startswith("linux"):
        pattern = "/opt/st/stm32cubeide*/plugins/com.st.stm32cube.ide.mcu.externaltools.openocd.*/tools/bin/openocd"
    else:
        pattern = ""
    if pattern:
        matches = glob.glob(pattern)
        if matches:
            openocd_bin = matches[0]
    os.environ["OPENOCD_BIN"] = openocd_bin
