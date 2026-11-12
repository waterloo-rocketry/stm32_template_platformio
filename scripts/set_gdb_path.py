#!/usr/bin/env python3
"""Write this machine's PlatformIO ARM GCC folder into .vscode/launch.json."""
import glob
import os
import re
import sys

try:
    Import("env")  # set when PlatformIO runs this file; SCons does not define __file__
    ROOT = env.subst("$PROJECT_DIR")
except NameError:
    ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LAUNCH = os.path.join(ROOT, ".vscode", "launch.json")
PACKAGE = re.compile(r"toolchain-gccarmnoneeabi(?:@[A-Za-z0-9.]+)?")


def spec():
    ini = os.path.join(ROOT, "platformio.ini")
    with open(ini, encoding="utf-8") as handle:
        for line in handle:
            line = line.split(";", 1)[0]
            marker = "toolchain-gccarmnoneeabi@"
            if marker in line:
                return line.split(marker, 1)[1].split()[0].lstrip("~^")
    return ""


def version_of(package_dir):
    name = os.path.basename(package_dir)
    if "@" in name:
        return name.split("@", 1)[1]
    manifest = os.path.join(package_dir, "package.json")
    if not os.path.isfile(manifest):
        return ""
    with open(manifest, encoding="utf-8") as handle:
        for line in handle:
            if '"version"' in line:
                return line.split(":", 1)[1].strip().strip('",')
    return ""


def matches(version, wanted):
    if not wanted:
        return False
    head = wanted.rsplit(".", 1)[0]
    return version == wanted or version.startswith(head + ".")


def installed_package():
    exe = "arm-none-eabi-gdb.exe" if os.name == "nt" else "arm-none-eabi-gdb"
    pattern = os.path.join(os.path.expanduser("~"), ".platformio", "packages", "toolchain-gccarmnoneeabi*", "bin", exe)
    found = [os.path.dirname(os.path.dirname(path)) for path in glob.glob(pattern)]
    if not found:
        return ""
    wanted = spec()
    matched = [path for path in found if matches(version_of(path), wanted)]
    return sorted(matched or found)[-1]


def slash(path):
    return path.replace("\\", "/")


def windows_stlink(text):
    # Cortex-Debug must spawn ST-LINK_gdbserver.exe. A .cmd exits and the session dies.
    if os.name != "nt":
        return text
    sys.path.insert(0, os.path.join(ROOT, "scripts"))
    import stlink_gdbserver
    try:
        server = slash(stlink_gdbserver.find_server())
        programmer = slash(stlink_gdbserver.find_programmer())
    except SystemExit:
        print("ST-Link tools not found; server path left unchanged")
        return text
    text = re.sub(
        r'("windows"\s*:\s*\{[^}]*?"serverpath"\s*:\s*")[^"]*(")',
        lambda match: match.group(1) + server + match.group(2),
        text,
        count=1,
        flags=re.DOTALL,
    )
    text = re.sub(
        r'("stm32cubeprogrammer"\s*:\s*")[^"]*(")',
        lambda match: match.group(1) + programmer + match.group(2),
        text,
        count=1,
    )
    print(server)
    return text


def main():
    if not os.path.isfile(LAUNCH):
        print("launch.json not found")
        return
    with open(LAUNCH, encoding="utf-8") as handle:
        original = handle.read()
    text = original
    package_dir = installed_package()
    if package_dir:
        name = os.path.basename(package_dir)
        text = PACKAGE.sub(name, text)
        print(name)
    else:
        print("ARM GCC package not found; compiler path left unchanged")
    text = windows_stlink(text)
    if text != original:
        with open(LAUNCH, "w", encoding="utf-8") as handle:
            handle.write(text)


main()
