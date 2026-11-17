#!/usr/bin/env bash
set -e

echo "=========================================================="
echo " Starting TruthLens Production Engine (PSAIAC_61)"
echo " Milestone: 100% Final Review Release"
echo "=========================================================="

# Start FastAPI microservice in background on port 8000
echo "Starting FastAPI REST API on port 8000..."
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --workers 2 &
FASTAPI_PID=$!

# Start Streamlit UI on port 8501
echo "Starting Streamlit UI on port 8501..."
streamlit run app.py \
    --server.port 8501 \
    --server.address 0.0.0.0 \
    --server.headless true \
    --server.enableCORS false \
    --server.enableXsrfProtection false \
    --theme.base dark &
STREAMLIT_PID=$!

echo "Both services launched successfully!"
echo "FastAPI PID: $FASTAPI_PID | Streamlit PID: $STREAMLIT_PID"

# Wait on all background jobs
wait -n $FASTAPI_PID $STREAMLIT_PID
