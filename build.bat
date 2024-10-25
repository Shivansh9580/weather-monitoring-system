@echo off

:: Step 1: Check Python version
python --version
IF %ERRORLEVEL% NEQ 0 (
    echo Python is not installed or not added to PATH. Exiting...
    pause
    exit /b 1
)

:: Step 2: Check if virtual environment exists, if not create one
IF NOT EXIST "venv\Scripts\activate" (
    echo Creating virtual environment...
    python -m venv venv
    IF %ERRORLEVEL% NEQ 0 (
        echo Failed to create virtual environment.
        pause
        exit /b 1
    )
) ELSE (
    echo Virtual environment already exists.
)

:: Step 3: Activate the virtual environment
echo Activating virtual environment...
call venv\Scripts\activate
IF %ERRORLEVEL% NEQ 0 (
    echo Failed to activate virtual environment.
    pause
    exit /b 1
)

:: Step 4: Install dependencies
IF EXIST "requirements.txt" (
    echo Installing dependencies from requirements.txt...
    pip install -r requirements.txt
    IF %ERRORLEVEL% NEQ 0 (
        echo Failed to install dependencies.
        pause
        exit /b 1
    )
) ELSE (
    echo requirements.txt not found. Generating requirements.txt...
    pip freeze > requirements.txt
    IF %ERRORLEVEL% NEQ 0 (
        echo Failed to generate requirements.txt.
        pause
        exit /b 1
    )
    echo Dependencies saved to requirements.txt.
)

:: Step 5: Run the main script
echo Running Weather Monitoring System...
python weather_system.py
IF %ERRORLEVEL% NEQ 0 (
    echo Failed to run the script.
    pause
    exit /b 1
)

:: Deactivate virtual environment
deactivate

:: Keep the window open
echo Build process completed.
pause
