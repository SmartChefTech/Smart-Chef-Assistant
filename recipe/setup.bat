@echo off

REM Check if Conda is installed
if not exist "%USERPROFILE%\Anaconda3\Scripts\conda.exe" (
    echo Conda could not be found. Please install Conda and try again.
    exit /b 1
)

REM Check if the environment already exists
conda env list | find "recipe-app" > nul
if %errorlevel% equ 0 (
    echo Updating existing recipe-app environment...
    call conda env update -f conda-environment.yml
) else (
    echo Creating new recipe-app environment...
    call conda env create -f conda-environment.yml
)

REM Activate the environment
call conda activate recipe-app

REM Run the database setup script
python sqlite-database-setup.py

REM Run the web crawler to populate the database
python crawler.py

REM Run the unit tests
python -m unittest connector_test.py
python -m unittest crawler_test.py

echo Setup complete. You can now run the main application with: python main-recipe-app.py