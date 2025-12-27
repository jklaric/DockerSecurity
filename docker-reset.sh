#!/usr/bin/env bash
set -e

echo "[*] Stopping and removing all containers..."
sudo docker rm -f $(sudo docker ps -aq) 2>/dev/null || true

echo "[*] Removing all images..."
sudo docker rmi -f $(sudo docker images -aq) 2>/dev/null || true

echo "[*] Removing all volumes..."
sudo docker volume rm $(sudo docker volume ls -q) 2>/dev/null || true

echo "[*] Removing user-defined networks..."
sudo docker network rm $(sudo docker network ls -q | grep -v -E 'bridge|host|none') 2>/dev/null || true

echo "[*] Pruning build cache..."
sudo docker builder prune -a -f

echo "[✓] Docker reset complete"
