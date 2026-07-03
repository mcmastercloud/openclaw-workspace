---
name: docker-management
description: Manage Docker-based services and tasks, including Firefly III database backups via the Docker Manager API. Use this to list available backups or trigger new ones.
---

# Docker Management

Manage Docker-based services, specifically tasks related to Firefly III backups via the Docker Manager API.

## Configuration

The following environment variables must be defined on the host:
- `DOCKER1_MANAGER_URL`: The full URL to the management API (e.g., `https://192.168.50.201:8085`).
- `DOCKER1_MANAGER_TOKEN`: The bearer token for authentication.

## Commands

### List Backups
Retrieve a manifest of all available Firefly III database backups.
```bash
curl -k -X POST "$DOCKER1_MANAGER_URL" \
  -H "Authorization: Bearer $DOCKER1_MANAGER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"command": "list-backups"}'
```

### Create Backup
Trigger a new backup of the Firefly III database.
```bash
curl -k -X POST "$DOCKER1_MANAGER_URL" \
  -H "Authorization: Bearer $DOCKER1_MANAGER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"command": "backup-firefly"}'
```
