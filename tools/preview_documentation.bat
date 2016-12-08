@echo off

cd docs
call .\make.bat html
cd build\html
call python -m http.server 80
cd ..\..\..\
