@echo OFF

echo "Performing first-time setup."
echo "Installing python 3.6.6..."

reg Query "HKLM\Hardware\Description\System\CentralProcessor\0" | find /i "x86" > NUL && set OS=32BIT || set OS=64BIT

cd installers

if %OS%==32BIT (
    python-3.6.6.exe /quiet /PrependPath=1
)
if %OS%==64BIT (
    python-3.6.6-amd64.exe /quiet /PrependPath=1
)

cd ..

echo "Installing necessary packages..."

python setup.py