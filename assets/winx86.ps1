Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
choco install curl
curl 'https://github.com/MangDL/MangDL/releases/download/0.0.0-alpha.4/mangdl-winx86.zip' -o mangdl.zip
tar -xf mangdl.zip -C C:\
Remove-Item -Force mangdl.zip
"Set-Alias -Name mangdl -Value C:\mangdl\mangdl.bat" >> $PROFILE.CurrentUserAllHosts
. $PROFILE.CurrentUserAllHosts