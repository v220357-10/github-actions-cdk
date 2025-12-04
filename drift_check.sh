!/usr/bin/env bash
set -euo pipefail
STACK_NAME="$1"
REGION="$2"

DETECT_ID=$(aws cloudformation detect-stack-drift \
  --stack-name "$STACK_NAME" --region "$REGION" \
  --query StackDriftDetectionId --output text)

echo "Started drift detection: $DETECT_ID"
STATUS="DETECTION_IN_PROGRESS"
while [ "$STATUS" = "DETECTION_IN_PROGRESS" ]; do
  sleep 5
  STATUS=$(aws cloudformation describe-stack-drift-detection-status \
    --stack-drift-detection-id "$DETECT_ID" \
    --region "$REGION" \
    --query DetectionStatus --output text)
  echo "Status: $STATUS"
done

DRIFT_STATUS=$(aws cloudformation describe-stack-drift-detection-status \
  --stack-drift-detection-id "$DETECT_ID" \
  --region "$REGION" \
  --query StackDriftStatus --output text)

echo "Stack drift status: $DRIFT_STATUS"
if [ "$DRIFT_STATUS" = "DRIFTED" ]; then
  exit 2
fi