# SPDX-FileCopyrightText: 2026 GNU APMG contributors
# SPDX-License-Identifier: GPL-3.0-only
param(
    [Parameter(Mandatory=$true)][string]$SessionDirectory,
    [Parameter(Mandatory=$true)][string]$DecisionsFile,
    [Parameter(Mandatory=$true)][string]$Actor
)
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$python = Join-Path $root '.venv-phase2\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $python)) { throw 'Environnement Phase 2 introuvable.' }
$session = (Resolve-Path -LiteralPath $SessionDirectory).Path
$decisions = (Resolve-Path -LiteralPath $DecisionsFile).Path
Push-Location -LiteralPath $root
try {
    & $python -X utf8 -m photosemantique.review apply $session --decisions $decisions --actor $Actor
    if ($LASTEXITCODE) { exit $LASTEXITCODE }
    & $python -X utf8 -m photosemantique.review render $session
    if ($LASTEXITCODE) { exit $LASTEXITCODE }
    & $python -X utf8 -m photosemantique.review status $session
    if ($LASTEXITCODE) { exit $LASTEXITCODE }
    Write-Host 'Decisions importees. Fermez puis rouvrez review.html pour poursuivre la revue.'
}
finally { Pop-Location }
