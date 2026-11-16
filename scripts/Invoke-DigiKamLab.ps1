# SPDX-FileCopyrightText: 2026 GNU APMG contributors
# SPDX-License-Identifier: GPL-3.0-only
param(
    [ValidateSet('Prepare','Open','Compare')][string]$Action = 'Open',
    [string]$LabDirectory = '',
    [string]$ReferenceExport = '',
    [string]$DigiKam = ''
)
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$workspace = Split-Path $root -Parent
if (-not $LabDirectory) { $LabDirectory = Join-Path $workspace 'etat-prive\digikam-lab-20261115' }
if (-not $ReferenceExport) { $ReferenceExport = Join-Path $workspace 'etat-prive\export-xmp-20261115' }
if (-not $DigiKam) { $DigiKam = Join-Path $workspace 'outils-locaux\digikam-9.1.0\digiKam\digikam.exe' }
$python = Join-Path $root '.venv-phase2\Scripts\python.exe'
Push-Location -LiteralPath $root
try {
    if ($Action -eq 'Prepare') {
        & $python -X utf8 -m photosemantique.digikam_lab prepare --export $ReferenceExport --lab $LabDirectory
        if ($LASTEXITCODE) { throw 'Preparation refusee.' }
    } elseif ($Action -eq 'Compare') {
        & $python -X utf8 -m photosemantique.digikam_lab compare --lab $LabDirectory
        if ($LASTEXITCODE) { throw 'Comparaison refusee.' }
    } else {
        if (Get-Process -Name digikam -ErrorAction SilentlyContinue) { throw 'Fermez digiKam avant de lancer le laboratoire.' }
        $lab = (Resolve-Path -LiteralPath $LabDirectory).Path
        $config = Join-Path $lab 'config\digikamrc'
        $database = Join-Path $lab 'database'
        foreach ($item in @($DigiKam,$config,(Join-Path $lab 'baseline.json'))) {
            if (-not (Test-Path -LiteralPath $item -PathType Leaf)) { throw "Fichier manquant : $item" }
        }
        if (-not (Test-Path -LiteralPath $database -PathType Container)) { throw 'Base du laboratoire manquante.' }
        Write-Host "Collection unique a choisir dans l'assistant : $(Join-Path $lab 'collection')"
        Write-Host "Base SQLite a confirmer : $database"
        Write-Host 'Suivre docs/tutorial/digikam-lab.md avant toute synchronisation.'
        # Windows Start-Process joins arguments: quote paths containing spaces.
        Start-Process -FilePath $DigiKam -ArgumentList @('--config',('"'+$config+'"'),'--database-directory',('"'+$database+'"')) -WindowStyle Hidden
    }
} finally { Pop-Location }
