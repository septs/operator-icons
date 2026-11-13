#!/usr/bin/env python3
import tomllib
from pathlib import Path

root = Path(__file__).parent.parent


def assert_icon(path: Path):
    assert path.is_file(), "operator icon files MUST BE a file"
    assert path.suffix == ".png", "operator icon files MUST BE .PNG"
    data = path.read_bytes()
    assert len(data) >= 33, "operator icon files MUST BE at least 33 bytes"
    assert data.startswith(b"\x89PNG\r\n\x1a\n"), "operator icon files MUST BE starts with PNG signature"
    width = int.from_bytes(data[16:20], "big")
    height = int.from_bytes(data[20:24], "big")
    assert 256 <= width <= 1024, "operator icon files MUST BE between 256 and 1024 pixels"
    assert 256 <= height <= 1024, "operator icon files MUST BE between 256 and 1024 pixels"
    assert width == height, "operator icon files MUST BE square"


def assert_catalog(catalog_path: Path):
    data: dict = tomllib.loads(catalog_path.read_text())
    assert "operators" in data, "catalog missing operators"
    for operator in data.get("operators", []):
        entries = [operator, *operator.get("gids", [])]
        for entry in entries:
            icon = entry.get("icon")
            icon_scope = entry.get("icon_scope")
            assert bool(icon) == bool(icon_scope), "icon and icon_scope MUST BE set together"
            if not icon:
                continue
            target = root / "icons" / icon_scope / f"{icon}.png"
            assert target.is_file(), "missing referenced icon {target}"


def main():
    icon_files = list[Path](root.rglob("icons/**/*.png"))
    catalog_files = list[Path](root.rglob("catalog/**/*.toml"))
    assert any(icon_files), "icons/: no PNG icon files found"
    assert any(catalog_files), "catalog/: no catalog files found"
    for icon_path in icon_files:
        try:
            assert_icon(icon_path)
        except AssertionError as e:
            raise AssertionError(f"{icon_path}: {e}") from e
    for catalog_path in catalog_files:
        try:
            assert_catalog(catalog_path)
        except (AssertionError, TypeError) as e:
            raise AssertionError(f"{catalog_path}: {e}") from e
    print(f"Validated {len(icon_files)} PNG icons and {len(catalog_files)} catalog files.")


if __name__ == "__main__":
    main()
