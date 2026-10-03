$ImageName = "vehicle-rental-service:v1.0.0"

Write-Host "`n[1/2] Scanning Repository Filesystem..." -ForegroundColor Yellow
docker run --rm -v "${PWD}:/apps" aquasec/trivy:latest fs --severity HIGH,CRITICAL /apps

Write-Host "`n[2/2] Scanning Docker Image: $ImageName..." -ForegroundColor Yellow
$imageExists = docker images -q $ImageName
if (-not $imageExists) {
    Write-Host "Building Docker image $ImageName..." -ForegroundColor Green
    docker build -t $ImageName vehicle-rental-service
}

docker save -o trivy-scan.tar $ImageName
docker run --rm -v "${PWD}:/apps" aquasec/trivy:latest image --input /apps/trivy-scan.tar --severity HIGH,CRITICAL
if (Test-Path trivy-scan.tar) {
    Remove-Item -Force trivy-scan.tar
}

Write-Host "`nTrivy scan complete." -ForegroundColor Cyan
