#!/usr/bin/env python3
import json
import tomllib
from pathlib import Path
from typing import Iterable
from zipfile import ZipFile, ZIP_DEFLATED, ZIP_STORED

root = Path(__file__).parent.parent


def build_manifest() -> Iterable[dict]:
    for definition in root.glob("catalog/*.toml"):
        try:
            data = tomllib.loads(definition.read_text(encoding="utf-8"))
        except Exception as error:
            raise RuntimeError(f"{definition}: invalid TOML: {error}") from error
        yield data


def create_bundle(saved_bundle_path: Path):
    with ZipFile(saved_bundle_path, "w") as bundle:
        bundle.write(root / "README.md", "README.md",
                     compress_type=ZIP_DEFLATED, compresslevel=9)
        bundle.writestr("manifest.json",
                        json.dumps(list(build_manifest())),
                        compress_type=ZIP_DEFLATED, compresslevel=9)
        for file in root.glob("icons/**/*.png"):
            saved_path = file.relative_to(root)
            bundle.writestr(saved_path.as_posix(), file.read_bytes(),
                            compress_type=ZIP_STORED)


def main():
    create_bundle(root / "bundle.zip")


if __name__ == "__main__":
    main()
