#!/usr/bin/env python3
"""Write this machine's PlatformIO ARM GCC folder into .vscode/launch.json."""
import glob
import os
import re

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


def main():
    package_dir = installed_package()
    if not package_dir or not os.path.isfile(LAUNCH):
        print("ARM GCC package not found; launch.json left unchanged")
        return
    name = os.path.basename(package_dir)
    with open(LAUNCH, encoding="utf-8") as handle:
        text = handle.read()
    updated = PACKAGE.sub(name, text)
    if updated != text:
        with open(LAUNCH, "w", encoding="utf-8") as handle:
            handle.write(updated)
    print(name)


main()
