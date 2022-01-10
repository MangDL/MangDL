curl -L -o mangdl.AppImage https://github.com/MangDL/MangDL/releases/download/3.0.0.0/mangdl-linux-x86_64.AppImage
chmod +x ./mangdl.AppImage
./mangdl.AppImage --appimage-extract
rm -rf ./mangdl.AppImage
rm -rf /usr/share/mangdl
mv squashfs-root /usr/share/mangdl
echo '#! /bin/sh
"exec" "/usr/share/mangdl/usr/bin/python3.10" "$0" "$@"
# -*- coding: utf-8 -*-
import re
import sys
from mangdl.cli import cli
if __name__ == "__main__":
    sys.argv[0] = re.sub("r(-script\.pyw|\.exe)?$", "", sys.argv[0])
    sys.exit(cli())' > /usr/bin/mangdl
chmod +x /usr/bin/mangdl
rm -rf linux-install.sh