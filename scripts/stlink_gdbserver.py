#!/usr/bin/env python3
"""Find the ST-Link GDB server for this OS and exec it.

cortex-debug launches this instead of a machine-specific path. Set
STLINK_GDBSERVER or STM32_PROGRAMMER_BIN to skip the search.
"""
import glob
import os
import subprocess
import sys


def _newest(pattern):
    matches = glob.glob(pattern)
    return sorted(matches)[-1] if matches else None


def _first(patterns):
    for pattern in patterns:
        hit = _newest(pattern)
        if hit:
            return hit
    return None


def find_server():
    override = os.environ.get("STLINK_GDBSERVER")
    if override and os.path.isfile(override):
        return override
    exe = "ST-LINK_gdbserver.exe" if sys.platform == "win32" else "ST-LINK_gdbserver"
    if sys.platform == "darwin":
        patterns = [
            "/Applications/STM32CubeIDE.app/Contents/Eclipse/plugins/"
            "com.st.stm32cube.ide.mcu.externaltools.stlink-gdb-server.*/tools/bin/" + exe,
        ]
    elif sys.platform == "win32":
        patterns = [
            r"C:\ST\STM32CubeIDE*\STM32CubeIDE\plugins"
            r"\com.st.stm32cube.ide.mcu.externaltools.stlink-gdb-server.*\tools\bin" + "\\" + exe,
            r"C:\Program Files\STMicroelectronics\STM32CubeIDE*\STM32CubeIDE\plugins"
            r"\com.st.stm32cube.ide.mcu.externaltools.stlink-gdb-server.*\tools\bin" + "\\" + exe,
            r"C:\ST\STM32CubeCLT*\STLink-gdb-server\bin" + "\\" + exe,
        ]
    else:
        patterns = [
            "/opt/st/stm32cubeide*/plugins/"
            "com.st.stm32cube.ide.mcu.externaltools.stlink-gdb-server.*/tools/bin/" + exe,
            "/usr/local/STMicroelectronics/STLINK-gdb-server/bin/" + exe,
        ]
    found = _first(patterns)
    if not found:
        sys.stderr.write("ST-LINK_gdbserver not found. Install STM32CubeIDE or set STLINK_GDBSERVER.\n")
        sys.exit(1)
    return found


def find_programmer():
    override = os.environ.get("STM32_PROGRAMMER_BIN")
    if override and os.path.isdir(override):
        return override
    cli = "STM32_Programmer_CLI.exe" if sys.platform == "win32" else "STM32_Programmer_CLI"
    if sys.platform == "darwin":
        patterns = [
            "/Applications/STM32CubeIDE.app/Contents/Eclipse/plugins/"
            "com.st.stm32cube.ide.mcu.externaltools.cubeprogrammer.*/tools/bin/" + cli,
            "/Applications/STM32CubeProgrammer.app/Contents/MacOs/bin/" + cli,
            "/Applications/STM32CubeProgrammer.app/Contents/Resources/bin/" + cli,
        ]
    elif sys.platform == "win32":
        patterns = [
            r"C:\Program Files\STMicroelectronics\STM32Cube\STM32CubeProgrammer\bin" + "\\" + cli,
            r"C:\ST\STM32CubeIDE*\STM32CubeIDE\plugins"
            r"\com.st.stm32cube.ide.mcu.externaltools.cubeprogrammer.*\tools\bin" + "\\" + cli,
            r"C:\ST\STM32CubeCLT*\STM32CubeProgrammer\bin" + "\\" + cli,
        ]
    else:
        patterns = [
            "/usr/local/STMicroelectronics/STM32Cube/STM32CubeProgrammer/bin/" + cli,
            "/opt/st/stm32cubeide*/plugins/"
            "com.st.stm32cube.ide.mcu.externaltools.cubeprogrammer.*/tools/bin/" + cli,
        ]
    found = _first(patterns)
    if not found:
        sys.stderr.write("STM32_Programmer_CLI not found. Install STM32CubeIDE or set STM32_PROGRAMMER_BIN.\n")
        sys.exit(1)
    return os.path.dirname(found)


def main():
    server = find_server()
    programmer = find_programmer()
    args = sys.argv[1:]
    if os.environ.get("STLINK_DRY_RUN"):
        print(server)
        print(programmer)
        return
    if "-cp" in args:
        index = args.index("-cp")
        if index + 1 < len(args):
            args[index + 1] = programmer
        else:
            args.append(programmer)
    else:
        args.extend(["-cp", programmer])
    # The server loads ./native next to itself. cortex-debug's cwd is scripts/.
    os.chdir(os.path.dirname(server))
    if os.name == "nt":
        # os.execv on Windows returns immediately, so the .cmd exits and
        # Cortex-Debug kills the server. Wait until the server exits.
        raise SystemExit(subprocess.call([server] + args))
    os.execv(server, [server] + args)


if __name__ == "__main__":
    main()
