import subprocess

api_service = """[Unit]
Description=TruthLens FastAPI REST Microservice
After=network.target

[Service]
Type=simple
User=shubh
WorkingDirectory=/home/shubh/truth-lens
Environment="PATH=/home/shubh/truth-lens/venv/bin:/usr/local/bin:/usr/bin"
Environment="PYTHONPATH=/home/shubh/truth-lens"
ExecStart=/home/shubh/truth-lens/venv/bin/uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --workers 2
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
"""

ui_service = """[Unit]
Description=TruthLens Streamlit UI Dashboard
After=network.target truthlens-api.service

[Service]
Type=simple
User=shubh
WorkingDirectory=/home/shubh/truth-lens
Environment="PATH=/home/shubh/truth-lens/venv/bin:/usr/local/bin:/usr/bin"
Environment="PYTHONPATH=/home/shubh/truth-lens"
ExecStart=/home/shubh/truth-lens/venv/bin/streamlit run app.py --server.port 8501 --server.address 0.0.0.0 --server.headless true --theme.base dark --server.enableCORS false --server.enableXsrfProtection false
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
"""

nginx_conf = """server {
    listen 80 default_server;
    listen [::]:80 default_server;

    server_name _;

    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /health {
        proxy_pass http://127.0.0.1:8000/health;
        proxy_set_header Host $host;
    }

    location /docs {
        proxy_pass http://127.0.0.1:8000/docs;
        proxy_set_header Host $host;
    }

    location /openapi.json {
        proxy_pass http://127.0.0.1:8000/openapi.json;
        proxy_set_header Host $host;
    }

    location / {
        proxy_pass http://127.0.0.1:8501;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_read_timeout 86400;
    }
}
"""

def write_remote(remote_path, content):
    cmd = f"gcloud compute ssh truthlens-vm --zone=asia-south1-a --command=\"sudo python3 -c \\\"import sys; open('{remote_path}', 'w').write(sys.stdin.read())\\\"\" --quiet"
    p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, err = p.communicate(input=content)
    print(f"Wrote {remote_path}: code={p.returncode}")
    if err:
        print(f"Err: {err}")

write_remote("/etc/systemd/system/truthlens-api.service", api_service)
write_remote("/etc/systemd/system/truthlens-ui.service", ui_service)
write_remote("/etc/nginx/sites-available/default", nginx_conf)

# Reload daemon and restart services
subprocess.run(
    "gcloud compute ssh truthlens-vm --zone=asia-south1-a --command=\"sudo systemctl daemon-reload && sudo systemctl enable truthlens-api truthlens-ui nginx && sudo systemctl restart truthlens-api truthlens-ui nginx\" --quiet",
    shell=True
)
print("Services enabled and restarted successfully!")
