# SPDX-FileCopyrightText: 2026 GNU APMG contributors
# SPDX-License-Identifier: GPL-3.0-only
param([switch]$DownloadVisionModel, [switch]$DownloadOcrModels)
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$python = Join-Path $root '.venv-phase2\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $python)) {
    & python -m venv (Join-Path $root '.venv-phase2')
    if ($LASTEXITCODE) { exit $LASTEXITCODE }
}
& $python -m pip install --no-cache-dir -r (Join-Path $root 'requirements-phase2-windows.lock.txt')
if ($LASTEXITCODE) { exit $LASTEXITCODE }
if ($DownloadVisionModel) {
    & ollama pull qwen3-vl:8b
    if ($LASTEXITCODE) { exit $LASTEXITCODE }
}
if ($DownloadOcrModels) {
    $env:PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK = 'True'
    & $python -c "from paddleocr import PaddleOCR; PaddleOCR(device='cpu', enable_mkldnn=False, text_detection_model_name='PP-OCRv5_mobile_det', text_recognition_model_name='latin_PP-OCRv5_mobile_rec', use_doc_orientation_classify=False, use_doc_unwarping=False, use_textline_orientation=False)"
    if ($LASTEXITCODE) { exit $LASTEXITCODE }
}
Write-Host 'Installation terminee. Les telechargements de modeles ne font aucune analyse de photos.'
