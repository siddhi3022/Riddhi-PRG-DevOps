pipeline {
    agent any

    environment {
        APP        = 'vehicle-rental-service'
        NS         = 'vehicle-rental-system'
        MON        = 'monitoring'
        IMAGE      = 'vehicle-rental-service:v1.0.0'
        KUBECONFIG = 'C:/Users/Riddhi siddhi/.kube/config'
    }

    stages {
        stage('Cleanup & Run Tests') {
            steps {
                bat '''
                    powershell -NoProfile -Command "Get-NetTCPConnection -LocalPort 1000,1001,1002 -ErrorAction SilentlyContinue | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }; exit 0"
                    python -m pip install -r vehicle-rental-service/requirements.txt
                    python -m pytest vehicle-rental-service/tests -v
                '''
            }
        }

        stage('Build & Load Docker Image') {
            steps {
                bat '''
                    docker build -t %IMAGE% vehicle-rental-service
                    minikube status >nul 2>&1 && (
                        echo Loading %IMAGE% into minikube cluster via minikube image load...
                        minikube image load %IMAGE%
                    ) || (
                        docker save -o k8s.tar %IMAGE%
                        docker inspect minikube >nul 2>&1 && (
                            echo Loading %IMAGE% into minikube container...
                            docker cp k8s.tar minikube:/k8s.tar
                            docker exec minikube ctr -n k8s.io images import /k8s.tar
                            docker exec minikube rm -f /k8s.tar
                        )
                        docker inspect desktop-control-plane >nul 2>&1 && (
                            echo Loading %IMAGE% into desktop-control-plane container...
                            docker cp k8s.tar desktop-control-plane:/k8s.tar
                            docker exec desktop-control-plane ctr -n k8s.io images import /k8s.tar
                            docker exec desktop-control-plane rm -f /k8s.tar
                        )
                        if exist k8s.tar del /f /q k8s.tar
                    )
                '''
            }
        }

        stage('Trivy Security Scan') {
            steps {
                bat '''
                    echo [1/2] Scanning Repository Filesystem...
                    docker run --rm -v "%CD%:/apps" aquasec/trivy:latest fs --severity HIGH,CRITICAL /apps

                    echo [2/2] Scanning Docker Image %IMAGE%...
                    docker save -o trivy-scan.tar %IMAGE%
                    docker run --rm -v "%CD%:/apps" aquasec/trivy:latest image --input /apps/trivy-scan.tar --severity HIGH,CRITICAL
                    if exist trivy-scan.tar del /f /q trivy-scan.tar
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                bat '''
                    if not defined KUBECONFIG if exist "C:\\Users\\Riddhi siddhi\\.kube\\config" set KUBECONFIG=C:\\Users\\Riddhi siddhi\\.kube\\config
                    kubectl apply -f kubernetes/namespace.yaml
                    kubectl apply -f kubernetes/monitoring/namespace.yaml
                    kubectl apply -f kubernetes/vehicle-rental-service-deployment.yaml
                    kubectl apply -f kubernetes/vehicle-rental-service.yaml
                    kubectl apply -f kubernetes/monitoring/prometheus.yaml
                    kubectl apply -f kubernetes/monitoring/grafana.yaml
                    kubectl rollout restart deployment/%APP% -n %NS%
                    kubectl rollout restart deployment/prometheus -n %MON%
                    kubectl rollout status deployment/%APP% -n %NS% --timeout=120s
                    kubectl rollout status deployment/prometheus -n %MON% --timeout=60s
                '''
            }
        }

        stage('Start Services') {
            steps {
                bat '''
                    if not defined KUBECONFIG if exist "C:\\Users\\Riddhi siddhi\\.kube\\config" set KUBECONFIG=C:\\Users\\Riddhi siddhi\\.kube\\config
                    set JENKINS_NODE_COOKIE=dontKillMe
                    powershell -NoProfile -Command "Get-NetTCPConnection -LocalPort 1000,1001,1002 -ErrorAction SilentlyContinue | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }; exit 0"
                    start /B kubectl port-forward service/prometheus 1000:1000 -n %MON%
                    start /B kubectl port-forward service/vehicle-rental-service 1001:1001 -n %NS%
                    start /B kubectl port-forward service/grafana 1002:1002 -n %MON%
                    powershell -NoProfile -Command "Start-Sleep -Seconds 3"
                    exit /b 0
                '''
            }
        }
    }

    post {
        success {
            echo "Prometheus: http://localhost:1000"
            echo "API Docs:   http://localhost:1001/docs"
            echo "Grafana:    http://localhost:1002"
        }
        failure {
            echo "Pipeline failed!"
        }
    }
}
