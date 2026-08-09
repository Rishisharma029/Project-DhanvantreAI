# AuraMed AI — Production Deployment Guide ☁️

This guide outlines deployment steps for local Docker environments, PaaS providers (Railway, Render), and cloud infrastructure (AWS, GCP, Azure).

---

## 1. Docker Compose Production Stack (Recommended)

```bash
# Clone the repository
git clone https://github.com/Rishisharma029/Project-DhanvantreAI.git
cd Project-DhanvantreAI

# Launch 5-service container stack
docker compose up -d --build

# Verify container health
docker compose ps
```

---

## 2. Railway & Render PaaS Deployment

- **Railway**: Connect your GitHub repository to Railway. It will automatically detect [railway.json](file:///c:/Users/Rishi%20Sharma/OneDrive/Desktop/PRODUCTION/medical%20idea/railway.json) and deploy `backend/Dockerfile`.
- **Render**: Create a new Blueprint instance on Render and point it to [render.yaml](file:///c:/Users/Rishi%20Sharma/OneDrive/Desktop/PRODUCTION/medical%20idea/render.yaml).

---

## 3. Cloud Provider Deployments

- **AWS (App Runner / ECS Fargate)**: Use [deployment/aws/AppRunner.yaml](file:///c:/Users/Rishi%20Sharma/OneDrive/Desktop/PRODUCTION/medical%20idea/deployment/aws/AppRunner.yaml) or register [deployment/aws/ecs-task-definition.json](file:///c:/Users/Rishi%20Sharma/OneDrive/Desktop/PRODUCTION/medical%20idea/deployment/aws/ecs-task-definition.json) with AWS ECS.
- **Google Cloud (Cloud Run / App Engine)**: Deploy container using `gcloud run services replace deployment/gcp/cloudrun-service.yaml`.
- **Microsoft Azure (Container Apps)**: Deploy IaC template using `az deployment group create --resource-group auramed-rg --template-file deployment/azure/azure-container-app.bicep`.
