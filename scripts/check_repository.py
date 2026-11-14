# Vérification du blueprint et des exclusions évidentes avant publication (ne remplace pas un audit Git/secret).
# SPDX-FileCopyrightText: 2026 PhotoSémantique contributors
# SPDX-License-Identifier: GPL-3.0-only
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = ["README.md", "COPYING", "INSTALL.md", "CONTRIBUTING.md", "CODE_OF_CONDUCT.md", "MAINTAINERS.md", "ROADMAP.md", "GOVERNANCE.md", "SECURITY.md", "PRIVACY.md", "NOTICE", "third_party/manifest.json", "docs/validation/pilot-protocol.md"]
FORBIDDEN_EXT = {".jpg", ".jpeg", ".png", ".heic", ".tiff", ".raw", ".dng", ".cr2", ".nef", ".arw", ".gguf", ".onnx", ".safetensors", ".sqlite", ".db", ".key", ".pem"}


def validate():
    missing = [p for p in REQUIRED if not (ROOT / p).exists()]
    if missing: raise AssertionError(f"Fichiers manquants : {missing}")
    license_text = (ROOT / "COPYING").read_text(encoding="utf-8")
    if len(license_text) < 30000 or "GNU GENERAL PUBLIC LICENSE" not in license_text or "Version 3, 29 June 2007" not in license_text:
        raise AssertionError("COPYING doit contenir le texte intégral GPLv3")
    bad = [p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*") if p.is_file() and p.suffix.lower() in FORBIDDEN_EXT]
    if bad: raise AssertionError(f"Fichiers binaires/photos interdits dans le socle : {bad}")
    for p in (ROOT / "scripts").glob("*.py"):
        if "SPDX-License-Identifier: GPL-3.0-only" not in p.read_text(encoding="utf-8"):
            raise AssertionError(f"En-tête de licence absent dans {p}")
    print("Contrôles de structure et d'exclusion OK (contrôle partiel)")


if __name__ == "__main__": validate()
