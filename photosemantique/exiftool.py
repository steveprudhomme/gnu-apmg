"""Lecture EXIF/IPTC/XMP via un exécutable ExifTool local, sans écriture."""
# SPDX-FileCopyrightText: 2026 PhotoSémantique contributors
# SPDX-License-Identifier: GPL-3.0-only
from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path
from typing import Any


class ExifToolError(RuntimeError):
    """Erreur d'outil ou de fichier, capturée et journalisée par fichier."""


class ExifToolReader:
    def __init__(self, executable: str = "exiftool", timeout_seconds: int = 45) -> None:
        candidate = shutil.which(executable)
        if candidate is None:
            raise ExifToolError(f"ExifTool introuvable ({executable}). Installer ExifTool ou utiliser --no-exif explicitement.")
        self.executable = candidate
        self.timeout_seconds = timeout_seconds
        try:
            completed = subprocess.run([candidate, "-ver"], capture_output=True, text=True, timeout=10, check=False)
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise ExifToolError("ExifTool ne répond pas à -ver") from exc
        if completed.returncode != 0 or not completed.stdout.strip():
            raise ExifToolError("Impossible de déterminer la version ExifTool")
        self.version = completed.stdout.strip().splitlines()[0]

    def read(self, path: Path) -> dict[str, Any]:
        # -- évite qu'un nom de fichier commençant par - soit lu comme option.
        args = [self.executable, "-j", "-G1:4", "-a", "-s", "--", str(path)]
        try:
            completed = subprocess.run(args, capture_output=True, text=True, timeout=self.timeout_seconds, check=False, encoding="utf-8", errors="replace")
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise ExifToolError("ExifTool indisponible ou délai dépassé") from exc
        if completed.returncode != 0:
            raise ExifToolError(f"ExifTool a retourné le code {completed.returncode} (vérifier le fichier)")
        try:
            result = json.loads(completed.stdout)
        except json.JSONDecodeError as exc:
            raise ExifToolError("ExifTool a renvoyé un JSON invalide") from exc
        if not isinstance(result, list) or len(result) != 1 or not isinstance(result[0], dict):
            raise ExifToolError("Structure JSON ExifTool inattendue")
        # SourceFile est un chemin local et ne doit pas être interprété comme tag EXIF.
        data = {k: v for k, v in result[0].items() if k != "SourceFile" and not k.endswith(":SourceFile")}
        if any(k == "Error" or k.endswith(":Error") for k in data):
            raise ExifToolError("ExifTool signale une erreur dans les métadonnées")
        return data
