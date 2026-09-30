# Vehicle Rental System – DevOps Pipeline

Version: **v1.0.0**

A FastAPI-based Vehicle Rental System with vehicles, customers and bookings, automated CI/CD through Jenkins, Docker containerization, Kubernetes deployment, rollback support, monitoring, logging and Trivy security scanning.

## Features

- Vehicle CRUD APIs
- Customer CRUD APIs
- Booking APIs with vehicle/customer validation
- FastAPI Swagger documentation
- Health and metrics endpoints
- Pytest automated tests
- Docker image versioning
- Jenkins CI/CD
- Trivy HIGH/CRITICAL security scan
- Kubernetes deployment with readiness/liveness probes
- Kubernetes rollout history and rollback on pipeline failure
- Prometheus monitoring
- Grafana dashboard
- Kubernetes/application logging

## Ports

- Prometheus UI: **1000**
- Vehicle Rental API / Swagger: **1001**
- Grafana: **1002**
- Internal container ports: 8000 (app), 9090 (prometheus), 3000 (grafana)

## URLs

```text
http://localhost:1000         (Prometheus UI & Metrics)
http://localhost:1001/        (Vehicle Rental API)
http://localhost:1001/docs    (Swagger UI)
http://localhost:1001/health  (Health Check)
http://localhost:1001/metrics (Application Prometheus Metrics)
http://localhost:1002         (Grafana Observability Dashboard)
```

## API Endpoints

```text
GET/POST/PUT/DELETE /vehicles
GET/POST/PUT/DELETE /customers
GET/POST/PUT/DELETE /bookings
```

## CI/CD Pipeline

```text
Checkout
→ Versioning
→ Install Dependencies
→ Automated Tests
→ Dependency Validation
→ Docker Build
→ Trivy Security Scan
→ Image Verification
→ Kubernetes Preparation
→ Image Load
→ Deployment
→ Health/API Validation
→ Prometheus
→ Grafana
→ Monitoring/Logging Validation
→ Rollback Capability Check
→ Port Forwarding
```

On a failed pipeline after deployment, Jenkins attempts `kubectl rollout undo` for the Vehicle Rental deployment.

## Jenkins

The Jenkinsfile is written for a Windows Jenkins agent and uses `bat` commands. Docker Desktop and a working Kubernetes context are required.

## Kubernetes

Namespace:

```text
vehicle-rental-system
```

Application deployment:

```text
vehicle-rental-service
```

Monitoring namespace:

```text
monitoring
```
