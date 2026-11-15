# SPDX-FileCopyrightText: 2026 GNU APMG contributors
# SPDX-License-Identifier: GPL-3.0-only
param(
    [string]$ExifTool = '',
    [string]$Python = 'python'
)
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
if (-not $ExifTool) {
    $workspaceRoot = Split-Path $projectRoot -Parent
    $ExifTool = Join-Path $workspaceRoot 'outils-locaux\exiftool-13.63\exiftool-13.63_64\exiftool.exe'
}
if (-not (Test-Path -LiteralPath $ExifTool -PathType Leaf)) {
    throw 'ExifTool introuvable. Indiquez son chemin avec -ExifTool.'
}
$previousExifTool = $env:GNU_APMG_EXIFTOOL
$testExitCode = 1
Push-Location -LiteralPath $projectRoot
try {
    $env:GNU_APMG_EXIFTOOL = (Resolve-Path -LiteralPath $ExifTool).Path
    Write-Host 'Tests synthetiques uniquement : aucune photo privee analysee.'
    & $Python -X utf8 -m unittest discover -s tests -p 'test_*.py' -v
    $testExitCode = $LASTEXITCODE
}
finally {
    $env:GNU_APMG_EXIFTOOL = $previousExifTool
    Pop-Location
}
exit $testExitCode
