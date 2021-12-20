@ECHO off
pushd %~dp0
shift
set params=%1
:loop
shift
if [%1]==[] goto afterloop
set params=%params% %1
goto loop
:afterloop
python mangdl\mangdl.py %*
popd