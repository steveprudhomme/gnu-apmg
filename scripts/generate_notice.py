# Génération des mentions légales depuis le manifeste architectural (PAS un audit complet des dépendances).
# SPDX-FileCopyrightText: 2026 PhotoSémantique contributors
# SPDX-License-Identifier: GPL-3.0-only
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def render():
    manifest = json.loads((ROOT / "third_party/manifest.json").read_text(encoding="utf-8"))
    lines = ["NOTICE — GNU APMG", "", "Ce fichier est généré. Référence des composants envisagés ou installés séparément : AUCUN binaire tiers fourni", "par le dépôt ; ce fichier NE CONSTITUE PAS un SBOM de distribution.", "", "Voir COPYING pour la GNU GPL v3 du code original du projet.", ""]
    for component in sorted(manifest["components"], key=lambda c: c["name"].casefold()):
        lines += [f"- {component['name']}", f"  Licence : {component['license']}", f"  Source : {component['source']}", f"  Embarqué : {'oui' if component['bundled'] else 'non'}", f"  Réserve : {component['status']}", ""]
    return "\n".join(lines).rstrip() + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    target = ROOT / "NOTICE"
    expected = render()
    if args.check:
        if not target.exists() or target.read_text(encoding="utf-8") != expected:
            raise SystemExit("NOTICE obsolète : exécuter python scripts/generate_notice.py")
        print("NOTICE conforme au manifeste architectural")
    else:
        target.write_text(expected, encoding="utf-8")
        print("NOTICE généré")


if __name__ == "__main__":
    main()
