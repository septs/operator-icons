#!/usr/bin/env python3
import sys
import tomllib
from pathlib import Path

root = Path(__file__).parent.parent


def assert_icon(path: Path):
    png_signature = b"\x89PNG\r\n\x1a\n"

    if path.suffix.lower() != ".png":
        raise RuntimeError(f"{path}: operator icon files must be .PNG")

    data = path.read_bytes()
    if len(data) < 33 or not data.startswith(png_signature):
        raise RuntimeError(f"{path}: not a valid PNG file")

    width = int.from_bytes(data[16:20], "big")
    height = int.from_bytes(data[20:24], "big")
    if width != height:
        raise RuntimeError(f"{path}: icon must be square, got {width}x{height}")
    if width < 256 or width > 1024:
        raise RuntimeError(f"{path}: width must be between 256 and 1024, got {width}")
    if height < 256 or height > 1024:
        raise RuntimeError(f"{path}: height must be between 256 and 1024, got {height}")


def assert_catalog(catalog_path: Path):
    try:
        data = tomllib.loads(catalog_path.read_text())
    except Exception as error:
        raise RuntimeError(f"{catalog_path}: invalid TOML: {error}") from error

    for operator in data.get("operators", []):
        entries = [operator, *operator.get("gids", [])]
        for entry in entries:
            icon = entry.get("icon")
            icon_scope = entry.get("icon_scope")
            if bool(icon) != bool(icon_scope):
                raise RuntimeError(f"{catalog_path}: icon and icon_scope must be set together")
            if not icon:
                continue
            target = root / "icons" / icon_scope / f"{icon}.png"
            if not target.exists():
                raise RuntimeError(f"{catalog_path}: missing referenced icon {target}")


def main():
    png_files = []
    failures = []

    for path in root.rglob("icons/**/*.png"):
        try:
            assert_icon(path)
            png_files.append(path)
        except RuntimeError as e:
            failures.append(str(e))
    if not png_files:
        failures.append("icons/: no PNG icon files found")

    for catalog_path in sorted(root.rglob("catalog/**/*.toml")):
        try:
            assert_catalog(catalog_path)
        except RuntimeError as e:
            failures.append(str(e))

    if failures:
        print("\n".join(failures), file=sys.stderr)
        raise SystemExit(1)

    print(f"Validated {len(png_files)} PNG icons and {len(list(root.rglob('catalog/**/*.toml')))} catalog files.")


if __name__ == "__main__":
    main()
