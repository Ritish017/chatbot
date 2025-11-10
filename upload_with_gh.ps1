$ghPath = 'C:\Github CLI 2.65\gh_2.65.0_windows_amd64\bin\gh.exe'
$repo = 'Ritish017/chatbot'
$branch = 'main'

# Helper: recursively get all files in the repo from GitHub API
function Get-RemoteFiles($path = "") {
    $apiPath = if ($path) { "repos/$repo/contents/$path?ref=$branch" } else { "repos/$repo/contents?ref=$branch" }
    $result = & $ghPath api $apiPath | ConvertFrom-Json
    $files = @()
    foreach ($item in $result) {
        if ($item.type -eq "file") {
            $files += $item.path
        } elseif ($item.type -eq "dir") {
            $files += Get-RemoteFiles $item.path
        }
    }
    return $files
}

# 1. Delete all files from remote repo (except .gitignore/README.md if you want to keep them)
Write-Host "Fetching remote files to delete..."
$remoteFiles = Get-RemoteFiles
foreach ($remoteFile in $remoteFiles) {
    if ($remoteFile -notmatch "^(\.gitignore|README.md)$") {
        Write-Host "Deleting $remoteFile from remote repo..."
        # Get the file's SHA
        $fileInfo = & $ghPath api repos/$repo/contents/$remoteFile?ref=$branch | ConvertFrom-Json
        $sha = $fileInfo.sha
        & $ghPath api repos/$repo/contents/$remoteFile -X DELETE -F message="Delete $remoteFile" -F sha=$sha -F branch=$branch
    }
}

# 2. Upload local files, preserving folder structure
Write-Host "Uploading local files..."
$files = Get-ChildItem -Recurse -File | Where-Object { $_.FullName -notmatch '\\.git|__pycache__|\\.venv' }
foreach ($file in $files) {
    $relativePath = $file.FullName.Substring($PWD.Path.Length + 1) -replace "\\", "/"
    Write-Host "Uploading $relativePath..."
    $content = [Convert]::ToBase64String([IO.File]::ReadAllBytes($file.FullName))
    & $ghPath api repos/$repo/contents/$relativePath -X PUT -F message="Add $relativePath" -F content=$content -F branch=$branch
}

Write-Host "Upload complete."
