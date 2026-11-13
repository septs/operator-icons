#!/usr/bin/env python3
import json
import tomllib
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED, ZIP_STORED


def main(base_path: Path):
    saved_bundle_path = base_path / "bundle.zip"
    with ZipFile(saved_bundle_path, "w") as bundle:
        print("Creating bundle.zip...")
        bundle.compression = ZIP_DEFLATED
        bundle.compresslevel = 9
        for file in base_path.rglob("*"):
            saved_path = file.relative_to(base_path)
            if not file.is_file() or file.name == saved_bundle_path.name:
                continue  # ignore not files or the bundle itself
            if any(part.startswith(".") for part in saved_path.parts):
                continue  # ignore hidden files
            if file.suffix == ".toml":
                config = tomllib.loads(file.read_text(encoding="utf-8"))
                bundle.writestr(saved_path.with_suffix(".json").as_posix(), json.dumps(config))
            else:
                compress_type = ZIP_STORED if file.suffix == ".png" else ZIP_DEFLATED
                bundle.writestr(saved_path.as_posix(), file.read_bytes(), compress_type)
        print("Done!")


if __name__ == "__main__":
    main(Path(__file__).parent.parent)
