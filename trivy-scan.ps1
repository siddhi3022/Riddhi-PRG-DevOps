# Local Trivy Security Scan Script for PowerShell
$ImageName = "vehicle-rental-service:v1.0.0"

Write-Host "=======================================================" -ForegroundColor Cyan
Write-Host "         TRIVY SECURITY SCANNING UTILITY              " -ForegroundColor Cyan
Write-Host "=======================================================" -ForegroundColor Cyan

Write-Host "`n[1/2] Scanning Repository Filesystem for vulnerabilities..." -ForegroundColor Yellow
docker run --rm -v "${PWD}:/apps" aquasec/trivy:latest fs --severity HIGH,CRITICAL /apps

Write-Host "`n[2/2] Checking local Docker Image: $ImageName..." -ForegroundColor Yellow
$imageExists = docker images -q $ImageName
if (-not $imageExists) {
    Write-Host "Building Docker image $ImageName for scanning..." -ForegroundColor Green
    docker build -t $ImageName vehicle-rental-service
}

Write-Host "Scanning Container Image: $ImageName..." -ForegroundColor Yellow
docker save -o trivy-scan.tar $ImageName
docker run --rm -v "${PWD}:/apps" aquasec/trivy:latest image --input /apps/trivy-scan.tar --severity HIGH,CRITICAL
if (Test-Path trivy-scan.tar) {
    Remove-Item -Force trivy-scan.tar
}

Write-Host "`n=======================================================" -ForegroundColor Cyan
Write-Host "         TRIVY SCAN COMPLETE                           " -ForegroundColor Cyan
Write-Host "=======================================================" -ForegroundColor Cyan
