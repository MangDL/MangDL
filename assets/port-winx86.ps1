Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
choco install -y curl 7zip.install
curl 'https://github.com/MangDL/MangDL/releases/download/3.0.0.2/mangdl-winx86.zip' -o mangdl.zip
$FolderName = 'C:\mangdl\'
if (Test-Path $FolderName) {
    Remove-Item -Force -Recurse $FolderName
}
tar -xf mangdl.zip
Remove-Item -Force mangdl.zip