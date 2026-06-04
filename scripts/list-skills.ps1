# Requires -Version 5.1

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$Repo = Resolve-Path (Join-Path $ScriptDir "..")
$RepoPath = $Repo.Path

Get-ChildItem -Path (Join-Path $RepoPath "skills") -Filter "SKILL.md" -Recurse -File | 
    Where-Object { 
        $_.FullName -notmatch '\\node_modules\\' 
    } |
    ForEach-Object {
        $RelativePath = $_.FullName.Substring($RepoPath.Length + 1).Replace('\', '/')
        $RelativePath
    } | Sort-Object
