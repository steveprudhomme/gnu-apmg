# SPDX-FileCopyrightText: 2026 GNU APMG contributors
# SPDX-License-Identifier: GPL-3.0-only
param([Parameter(Mandatory=$true)][string]$ExportDirectory)
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
$python=Join-Path $root '.venv-phase2\Scripts\python.exe'
$directory=(Resolve-Path -LiteralPath $ExportDirectory).Path
Push-Location -LiteralPath $root
try {
    & $python -X utf8 -m photosemantique.xmp_export rollback $directory
    if ($LASTEXITCODE) { exit $LASTEXITCODE }
}
finally { Pop-Location }
