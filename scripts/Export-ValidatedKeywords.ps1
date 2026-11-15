# SPDX-FileCopyrightText: 2026 GNU APMG contributors
# SPDX-License-Identifier: GPL-3.0-only
param(
    [Parameter(Mandatory=$true)][string]$SessionDirectory,
    [Parameter(Mandatory=$true)][string]$ImagesDirectory,
    [Parameter(Mandatory=$true)][string]$Output,
    [switch]$PlanOnly
)
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
$python=Join-Path $root '.venv-phase2\Scripts\python.exe'
$session=(Resolve-Path -LiteralPath $SessionDirectory).Path
$images=(Resolve-Path -LiteralPath $ImagesDirectory).Path
$destination=[System.IO.Path]::GetFullPath($Output)
$command=if ($PlanOnly) {'plan'} else {'export'}
Push-Location -LiteralPath $root
try {
    & $python -X utf8 -m photosemantique.xmp_export $command --session $session --images $images --output $destination
    if ($LASTEXITCODE) { exit $LASTEXITCODE }
}
finally { Pop-Location }
