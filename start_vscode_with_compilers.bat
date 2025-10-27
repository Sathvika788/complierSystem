@echo off
echo Setting up compiler environment...
set PATH=C:\Program Files\OpenJDK\jdk-25\bin;%PATH%
set PATH=C:\Program Files\Go\bin;%PATH%
set PATH=C:\Program Files\dotnet;%PATH%
set PATH=C:\tools\ruby34\bin;%PATH%
echo Environment set! Starting VS Code...
code .
