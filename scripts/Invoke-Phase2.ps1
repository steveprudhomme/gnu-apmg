# SPDX-FileCopyrightText: 2026 GNU APMG contributors
# SPDX-License-Identifier: GPL-3.0-only
param(
    [Parameter(Mandatory=$true)][string]$SourceFile,
    [Parameter(Mandatory=$true)][string]$OutputDirectory,
    [switch]$Vision,
    [switch]$Ocr,
    [string]$Model = 'qwen3-vl:8b',
    [string]$DetectionModel = '',
    [string]$RecognitionModel = ''
)
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$python = Join-Path $root '.venv-phase2\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $python)) { throw 'Executez Setup-Phase2.ps1 avant ce script.' }
$source = (Resolve-Path -LiteralPath $SourceFile).Path
$output = [System.IO.Path]::GetFullPath($OutputDirectory)
if (Test-Path -LiteralPath $output) { throw 'Choisissez un nouveau dossier de sortie prive.' }
$prepared = Join-Path $output 'prepared'
if (-not $DetectionModel) { $DetectionModel = Join-Path $env:USERPROFILE '.paddlex\official_models\PP-OCRv5_mobile_det' }
if (-not $RecognitionModel) { $RecognitionModel = Join-Path $env:USERPROFILE '.paddlex\official_models\latin_PP-OCRv5_mobile_rec' }
Push-Location -LiteralPath $root
try {
    & $python -X utf8 -m photosemantique.phase2 prepare $source --output $prepared
    if ($LASTEXITCODE) { exit $LASTEXITCODE }
    if ($Vision) {
        & $python -X utf8 -m photosemantique.phase2 vision $prepared --model $Model --output (Join-Path $output 'vision.jsonl')
        if ($LASTEXITCODE) { exit $LASTEXITCODE }
    }
    if ($Ocr) {
        & $python -X utf8 -m photosemantique.phase2 ocr $prepared --detection $DetectionModel --recognition $RecognitionModel --output (Join-Path $output 'ocr.jsonl')
        if ($LASTEXITCODE) { exit $LASTEXITCODE }
    }
}
finally { Pop-Location }
