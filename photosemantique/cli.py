"""Interface en ligne de commande locale — Phase 1."""
# SPDX-FileCopyrightText: 2026 PhotoSémantique contributors
# SPDX-License-Identifier: GPL-3.0-only
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path
from urllib.parse import quote

from . import __version__
from .exiftool import ExifToolError
from .inventory import scan
from .storage import summary


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="gnu-apmg", description="Inventaire photo local, sans écriture sur les originaux")
    p.add_argument("--version", action="version", version=f"GNU APMG {__version__}")
    cmds = p.add_subparsers(dest="command", required=True)
    s = cmds.add_parser("scan", help="Découvrir, hacher et inventorier un dossier photo")
    s.add_argument("source", type=Path, help="Répertoire contenant des photos (lecture seule)")
    s.add_argument("--db", type=Path, required=True, help="Base SQLite hors sources et hors dépôt Git")
    s.add_argument("--exiftool", default="exiftool", help="Chemin de l'exécutable ExifTool local")
    s.add_argument("--no-exif", action="store_true", help="Ignorer volontairement l'extraction EXIF, pour un test limité")
    s.add_argument("--jsonl", type=Path, help="Manifeste JSON Lines privé (hors sources et dépôt Git)")
    r = cmds.add_parser("report", help="Statistiques sans chemins ni GPS en console")
    r.add_argument("--db", type=Path, required=True)
    return p


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.command == "scan":
            result = scan(root=args.source, db_path=args.db, exiftool=args.exiftool, no_exif=args.no_exif, jsonl_path=args.jsonl)
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 2 if result["errors"] else 0
        if not args.db.exists():
            raise ValueError("Base SQLite introuvable")
        db = sqlite3.connect(f"file:{quote(args.db.resolve().as_posix(), safe='/:')}?mode=ro", uri=True)
        try:
            print(json.dumps(summary(db), ensure_ascii=False, indent=2))
        finally:
            db.close()
        return 0
    except (OSError, ValueError, ExifToolError, sqlite3.Error) as exc:
        # Pas de trace complète ni de contenu EXIF dans la console par défaut.
        print(f"Erreur : {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
