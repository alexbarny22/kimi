# Пример будущего автодеплоя

Когда будут данные сервера, этот пример можно перенести в `.github/workflows/deploy.yml` и заполнить GitHub Secrets:

- `SERVER_HOST`
- `SERVER_USER`
- `SERVER_SSH_KEY`

```yaml
name: deploy

on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy over SSH
        uses: appleboy/ssh-action@v1
        with:
          host: ${{ secrets.SERVER_HOST }}
          username: ${{ secrets.SERVER_USER }}
          key: ${{ secrets.SERVER_SSH_KEY }}
          script: |
            set -e
            cd /path/to/kimi
            git pull origin main
            source .venv/bin/activate
            pip install -r requirements.txt
            sudo systemctl restart kimi-bot
```
