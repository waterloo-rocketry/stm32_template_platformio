import os
import sys
import glob
from SCons.Script import Import

Import("env")

# If OPENOCD_BIN is already defined in shell environment, use it
if "OPENOCD_BIN" in os.environ:
    sys.exit(0)

openocd_bin = "openocd"

if sys.platform == "darwin":
    pattern = "/Applications/STM32CubeIDE.app/Contents/Eclipse/plugins/com.st.stm32cube.ide.mcu.externaltools.openocd.*/tools/bin/openocd"
    matches = glob.glob(pattern)
    if matches:
        openocd_bin = matches[0]

elif sys.platform == "win32":
    pattern = r"C:\ST\STM32CubeIDE*\STM32CubeIDE\plugins\com.st.stm32cube.ide.mcu.externaltools.openocd.*\tools\bin\openocd.exe"
    matches = glob.glob(pattern)
    if matches:
        openocd_bin = matches[0]

elif sys.platform.startswith("linux"):
    pattern = "/opt/st/stm32cubeide*/plugins/com.st.stm32cube.ide.mcu.externaltools.openocd.*/tools/bin/openocd"
    matches = glob.glob(pattern)
    if matches:
        openocd_bin = matches[0]

os.environ["OPENOCD_BIN"] = openocd_bin