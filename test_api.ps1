# Test script to verify the API works after deployment
# Usage: .\test_api.ps1 [API_URL]
# Example: .\test_api.ps1 "https://your-app.up.railway.app"

param(
    [string]$ApiUrl = "http://localhost:8000"
)

Write-Host "Testing Hardscapes API at: $ApiUrl" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Test 1: Health check
Write-Host "`n1. Health Check (GET /):" -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$ApiUrl/" -Method Get
    $response | ConvertTo-Json
} catch {
    Write-Host "Failed: $_" -ForegroundColor Red
}

# Test 2: Get words for level 1
Write-Host "`n2. Get words for level 1 (GET /words?level=1&limit=5):" -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$ApiUrl/words?level=1&limit=5" -Method Get
    $response | ConvertTo-Json
} catch {
    Write-Host "Failed: $_" -ForegroundColor Red
}

# Test 3: Get stats
Write-Host "`n3. Get database stats (GET /stats):" -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$ApiUrl/stats" -Method Get
    $response | ConvertTo-Json
} catch {
    Write-Host "Failed: $_" -ForegroundColor Red
}

# Test 4: Custom parameters
Write-Host "`n4. Get words with custom parameters (level=5, min_len=4, max_len=6):" -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$ApiUrl/words?level=5&min_len=4&max_len=6&limit=3" -Method Get
    $response | ConvertTo-Json
} catch {
    Write-Host "Failed: $_" -ForegroundColor Red
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Testing complete!" -ForegroundColor Green
