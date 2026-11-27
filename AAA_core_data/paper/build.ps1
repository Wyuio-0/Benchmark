$ErrorActionPreference = 'Stop'
Push-Location $PSScriptRoot
try {
    & latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=_build paper_skeleton.tex
    if ($LASTEXITCODE -ne 0) { throw 'LaTeX build failed; see _build/paper_skeleton.log.' }
    Copy-Item -LiteralPath '_build/paper_skeleton.pdf' -Destination 'paper_skeleton.pdf' -Force
    $paperExportDir = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../output/pdf'))
    New-Item -ItemType Directory -Path $paperExportDir -Force | Out-Null
    Copy-Item -LiteralPath '_build/paper_skeleton.pdf' -Destination (Join-Path $paperExportDir 'paper_skeleton.pdf') -Force
    Write-Output "PDF ready: $(Join-Path $PSScriptRoot 'paper_skeleton.pdf')"
} finally {
    Pop-Location
}
