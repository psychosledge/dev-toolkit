# PSReadLine: prefix history search, menu completion, inline predictions
Set-PSReadLineKeyHandler -Key UpArrow -Function HistorySearchBackward
Set-PSReadLineKeyHandler -Key DownArrow -Function HistorySearchForward
Set-PSReadLineKeyHandler -Key Tab -Function MenuComplete
if (-not [Console]::IsOutputRedirected) {
    Set-PSReadLineOption -PredictionSource History -PredictionViewStyle ListView
}

$env:EDITOR = 'code --wait'
$env:VISUAL = $env:EDITOR

function eprof { code $PROFILE }

if (Get-Command gh -ErrorAction SilentlyContinue) {
    gh completion -s powershell | Out-String | Invoke-Expression
}
if (Get-Command mise -ErrorAction SilentlyContinue) {
    mise activate pwsh | Out-String | Invoke-Expression
}
if (Get-Command terraform -ErrorAction SilentlyContinue) {
    Set-Alias tf terraform
}

$localProfile = Join-Path $HOME 'profile.local.ps1'
if (Test-Path $localProfile) { . $localProfile }
