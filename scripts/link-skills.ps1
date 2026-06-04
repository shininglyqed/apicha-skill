# Requires -Version 5.1

# Links all skills in the repository to ~/.gemini/antigravity-cli/skills, 
# so that they can be used by the local Antigravity CLI.

$ErrorActionPreference = "Stop"

# Get Repo root (parent of parent of script)
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$Repo = Resolve-Path (Join-Path $ScriptDir "..")
$RepoPath = $Repo.Path

$Dest = Join-Path $HOME ".gemini\antigravity-cli\skills"

# Check if destination is a symbolic link or junction pointing to the repo
if (Test-Path $Dest) {
    $TargetInfo = Get-Item $Dest
    if ($TargetInfo.Attributes -match "ReparsePoint") {
        Write-Error "Error: $Dest is a symlink/junction. Remove it (Remove-Item `"$Dest`") and re-run this script."
    }
}

# Ensure destination directory exists
if (-not (Test-Path $Dest)) {
    New-Item -ItemType Directory -Path $Dest -Force | Out-Null
}

# Find all folders containing SKILL.md under $Repo/skills, excluding certain paths
$Skills = Get-ChildItem -Path (Join-Path $RepoPath "skills") -Filter "SKILL.md" -Recurse -File | 
    Where-Object { 
        $_.FullName -notmatch '\\node_modules\\'
    }

foreach ($SkillFile in $Skills) {
    $Src = $SkillFile.Directory.FullName
    $Name = $SkillFile.Directory.Name
    $Target = Join-Path $Dest $Name

    if (Test-Path $Target) {
        Remove-Item -Path $Target -Recurse -Force -ErrorAction SilentlyContinue
    }

    # Use Junction since it does not require Administrator privileges in Windows
    New-Item -ItemType Junction -Path $Target -Value $Src | Out-Null
    Write-Host "Linked $Name -> $Src"
}
