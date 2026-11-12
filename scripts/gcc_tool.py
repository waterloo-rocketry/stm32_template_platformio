#!/usr/bin/env python3
"""Run a PlatformIO ARM GCC tool without a version in launch.json.

The toolchain version lives in platformio.ini (platform_packages). This finds
that package under ~/.platformio/packages and execs the requested tool.
"""
import glob
import json
import os
import sys


def toolchain_spec():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ini = os.path.join(root, "platformio.ini")
    with open(ini, encoding="utf-8") as handle:
        for line in handle:
            line = line.split(";", 1)[0].strip()
            marker = "toolchain-gccarmnoneeabi@"
            if marker in line:
                return line.split(marker, 1)[1].split()[0]
    sys.stderr.write("platformio.ini does not name toolchain-gccarmnoneeabi.\n")
    sys.exit(1)


def matches(version, spec):
    if spec.startswith("~"):
        # ~1.120301.0 allows 1.120301.*
        head = spec[1:].rsplit(".", 1)[0]
        return version == spec[1:] or version.startswith(head + ".")
    if spec.startswith("^"):
        base = spec[1:]
        return version.split(".", 1)[0] == base.split(".", 1)[0] and version >= base
    return version == spec


def package_version(package_dir):
    name = os.path.basename(package_dir)
    if "@" in name:
        return name.split("@", 1)[1]
    manifest = os.path.join(package_dir, "package.json")
    if os.path.isfile(manifest):
        with open(manifest, encoding="utf-8") as handle:
            return json.load(handle).get("version", "")
    return ""


def find_tool(tool):
    override = os.environ.get("GCC_ARM_BIN")
    exe = tool + (".exe" if sys.platform == "win32" else "")
    if override:
        candidate = os.path.join(override, exe)
        if os.path.isfile(candidate):
            return candidate
    spec = toolchain_spec()
    pattern = os.path.join(os.path.expanduser("~"), ".platformio", "packages", "toolchain-gccarmnoneeabi*", "bin", exe)
    found = []
    for path in glob.glob(pattern):
        version = package_version(os.path.dirname(os.path.dirname(path)))
        if matches(version, spec):
            found.append((version, path))
    if not found:
        sys.stderr.write("No %s matching %s under ~/.platformio/packages.\n" % (exe, spec))
        sys.exit(1)
    return sorted(found)[-1][1]


def main():
    tool = sys.argv[1]
    for suffix in (".cmd", ".exe"):
        if tool.endswith(suffix):
            tool = tool[: -len(suffix)]
    binary = find_tool(tool)
    if os.environ.get("GCC_TOOL_DRY_RUN"):
        print(binary)
        return
    os.execv(binary, [binary] + sys.argv[2:])


if __name__ == "__main__":
    main()
