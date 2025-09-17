@echo off
REM Zendesk MCP Server Startup Script with .env loading

REM Load variables from .env file if it exists
if exist .env (
    echo Loading environment from .env file...
    for /f "usebackq tokens=1,2 delims==" %%a in (".env") do (
        set %%a=%%b
    )
) else (
    echo .env file not found, using default values...
    REM Set default values here
    set ZENDESK_BASE_URL=your_subdomain_here
    set ZENDESK_EMAIL=your_email_here
    set ZENDESK_API_TOKEN=your_api_token_here
)

echo.
echo Checking variable loading:
echo ZENDESK_BASE_URL=%ZENDESK_BASE_URL%
echo ZENDESK_EMAIL=%ZENDESK_EMAIL%
echo ZENDESK_API_TOKEN=%ZENDESK_API_TOKEN%
echo.

echo Starting MCP server on port 8021...
mcp-proxy --port 8021 --pass-environment -- mcp-zendesk

if %ERRORLEVEL% NEQ 0 pause