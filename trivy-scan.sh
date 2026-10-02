#!/usr/bin/env bash
# Local Trivy Security Scan Script for Bash
IMAGE_NAME="vehicle-rental-service:v1.0.0"

echo "======================================================="
echo "         TRIVY SECURITY SCANNING UTILITY              "
echo "======================================================="

echo ""
echo "[1/2] Scanning Repository Filesystem for vulnerabilities..."
docker run --rm -v "$(pwd):/apps" aquasec/trivy:latest fs --severity HIGH,CRITICAL /apps

echo ""
echo "[2/2] Scanning Docker Image: ${IMAGE_NAME}..."
if ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "Building image ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" vehicle-rental-service
fi

docker save -o trivy-scan.tar "${IMAGE_NAME}"
docker run --rm -v "$(pwd):/apps" aquasec/trivy:latest image --input /apps/trivy-scan.tar --severity HIGH,CRITICAL
rm -f trivy-scan.tar

echo ""
echo "======================================================="
echo "         TRIVY SCAN COMPLETE                           "
echo "======================================================="
