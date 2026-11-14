"""Point d'entrée `python -m photosemantique`."""
# SPDX-FileCopyrightText: 2026 PhotoSémantique contributors
# SPDX-License-Identifier: GPL-3.0-only
from .cli import main

if __name__ == "__main__":
    raise SystemExit(main())
