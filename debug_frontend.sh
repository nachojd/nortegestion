#!/bin/bash
# Debug script para frontend

echo "=== DEBUGGING FRONTEND CONTAINER ==="

# Check if container exists
echo "1. Checking if frontend container exists..."
docker ps -a | grep frontend

echo -e "\n2. Frontend container logs:"
docker logs nortegestion-frontend-1 2>&1 | tail -50

echo -e "\n3. Trying to exec into frontend container..."
docker exec nortegestion-frontend-1 ps aux 2>/dev/null || echo "Cannot exec into container"

echo -e "\n4. Testing health check manually..."
docker exec nortegestion-frontend-1 node -e "require('http').get('http://localhost:3000/', (res) => { console.log('Status:', res.statusCode); process.exit(res.statusCode === 200 ? 0 : 1); }).on('error', (err) => { console.log('Error:', err.message); process.exit(1); })" 2>/dev/null || echo "Health check failed"

echo -e "\n5. Check if port 3000 is listening..."
docker exec nortegestion-frontend-1 netstat -ln 2>/dev/null | grep 3000 || echo "Port 3000 not listening"

echo -e "\n6. Check filesystem..."
docker exec nortegestion-frontend-1 ls -la /app/ 2>/dev/null || echo "Cannot access /app/"