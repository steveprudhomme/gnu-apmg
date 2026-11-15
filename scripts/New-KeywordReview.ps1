# SPDX-FileCopyrightText: 2026 GNU APMG contributors
# SPDX-License-Identifier: GPL-3.0-only
param(
    [Parameter(Mandatory=$true)][string[]]$Observations,
    [Parameter(Mandatory=$true)][string]$SessionDirectory,
    [string[]]$PreparedDirectory = @(),
    [switch]$Open
)
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$python = Join-Path $root '.venv-phase2\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $python)) { throw 'Environnement Phase 2 introuvable.' }
$session = [System.IO.Path]::GetFullPath($SessionDirectory)
$arguments = @('-X','utf8','-m','photosemantique.review','create','--output',$session)
foreach ($file in $Observations) { $arguments += @('--input',(Resolve-Path -LiteralPath $file).Path) }
foreach ($directory in $PreparedDirectory) { $arguments += @('--prepared',(Resolve-Path -LiteralPath $directory).Path) }
Push-Location -LiteralPath $root
try {
    & $python @arguments
    if ($LASTEXITCODE) { exit $LASTEXITCODE }
    if ($Open) { Start-Process -FilePath (Join-Path $session 'review.html') | Out-Null }
}
finally { Pop-Location }
