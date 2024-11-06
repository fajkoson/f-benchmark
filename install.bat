@echo off

:: Check if Python is installed
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python to continue. > build.log
    echo Python is missing. See build.log for details.
    exit /b 1
)

:: Proceed with setup if Python is available
:: Create a virtual environment if it doesn't exist
if not exist ".venv" (
    python -m venv .venv
)

:: Activate the virtual environment
call .venv\Scripts\activate

:: Install Python dependencies from requirements.txt (if any)
pip install -r requirements.txt

:: Install Conan and Ninja if not already installed
pip install conan ninja

:: Run Conan to install dependencies
conan install . --output-folder=build --build=missing

:: Set up the build system (assuming Ninja)
cmake -B build -G Ninja
cmake --build build
