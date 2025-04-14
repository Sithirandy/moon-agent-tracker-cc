#!/bin/bash

echo "Running Integration Tests..."

# Wait briefly for new services to come up
sleep 20

# Example test — check if pods are running
kubectl get pods

# Example test — check health endpoints (replace with actual URLs if exposed)
for svc in agent-service integration-service notification-service aggregator-service
do
  HOST=$(kubectl get svc $svc -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')
  echo "Testing $svc at $HOST..."
  curl -sf http://$HOST/health || {
    echo "$svc failed health check"
    exit 1
  }
done

echo "✅ All integration tests passed."