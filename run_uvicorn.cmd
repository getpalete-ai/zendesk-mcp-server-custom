@echo off
REM Zendesk MCP Server with Direct Uvicorn Scaling for Windows

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

REM Configuration for scaling
if not defined WORKERS set WORKERS=4
if not defined HOST set HOST=0.0.0.0
if not defined PORT set PORT=8021
if not defined BACKLOG set BACKLOG=2048
if not defined TIMEOUT_KEEP_ALIVE set TIMEOUT_KEEP_ALIVE=30
if not defined LIMIT_CONCURRENCY set LIMIT_CONCURRENCY=1000

echo.
echo === Zendesk MCP Server - Uvicorn Scaling ===
echo Workers: %WORKERS%
echo Host: %HOST%
echo Port: %PORT%
echo Backlog: %BACKLOG%
echo Timeout Keep-Alive: %TIMEOUT_KEEP_ALIVE%
echo Concurrency Limit: %LIMIT_CONCURRENCY%
echo.
echo Checking variable loading:
echo ZENDESK_BASE_URL=%ZENDESK_BASE_URL%
echo ZENDESK_EMAIL=%ZENDESK_EMAIL%
echo ZENDESK_API_TOKEN=%ZENDESK_API_TOKEN%
echo.

echo Starting MCP server with %WORKERS% workers on %HOST%:%PORT%...
echo Note: Each worker can handle multiple concurrent requests via asyncio
echo Note: Connection pooling is enabled for better performance

REM Run uvicorn directly with our FastMCP server
uvicorn mcp_zendesk.server:app --host %HOST% --port %PORT% --workers %WORKERS% --backlog %BACKLOG% --timeout-keep-alive %TIMEOUT_KEEP_ALIVE% --limit-concurrency %LIMIT_CONCURRENCY% --log-level info

if %ERRORLEVEL% NEQ 0 pause
