# Weather App — Cloud Deployment & CI/CD Practice

A Django weather application integrated with Keycloak authentication, used as a cloud deployment practice project.

## Stack
- **Django** — weather app backend
- **Keycloak** — authentication (OIDC/OAuth2)
- **Docker + docker-compose** — containerization
- **AWS EC2** — cloud deployment (t2.micro free tier)
- **GitHub Actions** — CI/CD pipeline

## What this project covers

### Docker
- Dockerizing a Django application
- Multi-container setup with docker-compose (app + Keycloak)
- Container networking (service names vs localhost)
- Environment variable management across containers

### AWS
- Launching and managing an EC2 instance
- Security Groups and port management
- SSH key management
- Keeping the app running with systemd
- Elastic IP for stable public address ~~~~~--to-do

### CI/CD with GitHub Actions
- Automated testing on every push
- SSH deploy key setup
- GitHub Secrets for sensitive values
- Auto-deploy to AWS on push to main

## Project Structure
```
weather/          # Django app
  main/           # main app (views, models, auth)
  weather/        # Django project settings and urls
docker/           # Dockerfile and requirements.txt
.github/
  workflows/
    deploy.yml    # CI/CD pipeline
docker-compose.yaml
```

## Running locally
```bash
# start containers
docker-compose up

# app runs at http://localhost:8000/home/
# keycloak runs at http://localhost:7800
```

## Environment variables
Create a `.env` file in the project root:
```
OPENWEATHERMAP_API_KEY=your_key
KEYCLOAK_CLIENT_ID=your_client_id
KEYCLOAK_CLIENT_SECRET=your_secret
KEYCLOAK_REDIRECT_URI=http://localhost:8000/auth/callback/
KEYCLOAK_URL=http://keycloak-app:7800/realms/weather-app
KEYCLOAK_BROWSER_URL=http://localhost:7800/realms/weather-app
```

## CI/CD Pipeline
On every push to `main`:
1. GitHub spins up a fresh Ubuntu runner
2. Installs dependencies and runs Django tests
3. SSHs into AWS server
4. Pulls latest code and rebuilds Docker containers

Required GitHub Secrets: `SSH_PRIVATE_KEY`, `SERVER_IP`, and all env vars above.
