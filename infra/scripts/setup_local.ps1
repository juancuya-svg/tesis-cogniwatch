Copy-Item .env.example .env -ErrorAction SilentlyContinue
Docker compose up --build -d
Start-Sleep -Seconds 8
Docker compose exec backend python -m app.db.seed
Write-Host "CogniWatch local stack is ready."
