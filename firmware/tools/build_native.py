"""Build the firmware logic for the PC (unit tests and the protocol harness).

Uses the C++ compiler shipped in the `ziglang` package (dev dependency of api/), so no system
toolchain is needed. Run with the api environment:

    uv run --directory ../api python ../firmware/tools/build_native.py [unit_tests|harness]
"""

import shutil
import subprocess
import sys
from pathlib import Path

FIRMWARE = Path(__file__).resolve().parents[1]
CORE = FIRMWARE / "lib" / "av_core" / "src"
NATIVE = FIRMWARE / "test" / "native"
ARDUINOJSON = FIRMWARE / ".pio" / "libdeps" / "esp32dev" / "ArduinoJson" / "src"
OUT = FIRMWARE / ".pio" / "native"
EXE = ".exe" if sys.platform == "win32" else ""
TARGETS = {"unit_tests": NATIVE / "unit_tests.cpp", "harness": NATIVE / "harness.cpp"}


def _ensure_arduinojson() -> None:
    if (ARDUINOJSON / "ArduinoJson.h").is_file():
        return
    pio = shutil.which("pio") or str(Path.home() / ".local" / "bin" / f"pio{EXE}")
    subprocess.run([pio, "pkg", "install", "-e", "esp32dev", "-d", str(FIRMWARE)], check=True)


def _sources(entry: Path) -> list[Path]:
    return [*sorted(CORE.glob("*.cpp")), entry]


def build(target: str) -> Path:
    _ensure_arduinojson()
    entry = TARGETS[target]
    output = OUT / f"{target}{EXE}"
    inputs = [*_sources(entry), *CORE.glob("*.h"), *NATIVE.glob("*.h"), Path(__file__)]
    if output.exists() and all(p.stat().st_mtime <= output.stat().st_mtime for p in inputs):
        return output
    OUT.mkdir(parents=True, exist_ok=True)
    command = [
        sys.executable,
        "-m",
        "ziglang",
        "c++",
        "-std=c++17",
        "-O1",
        "-Wall",
        "-Wextra",
        "-Wno-unused-parameter",
        f"-I{CORE}",
        f"-I{NATIVE}",
        f"-I{ARDUINOJSON}",
        *[str(s) for s in _sources(entry)],
        "-o",
        str(output),
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        sys.stderr.write(result.stdout + result.stderr)
        raise SystemExit(f"falha ao compilar {target}")
    return output


if __name__ == "__main__":
    for name in sys.argv[1:] or list(TARGETS):
        print(build(name))
