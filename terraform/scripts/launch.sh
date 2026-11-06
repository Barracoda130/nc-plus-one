#!/bin/bash

set -euo pipefail
exec > >(tee -a /home/ubuntu/progress.txt) 2>&1

echo "Starting launch script"

echo "Updating apt package lists"
sudo apt update

echo "Changing to /home/ubuntu"
cd /home/ubuntu

echo "Installing required packages"
sudo apt install apache2 postgresql make python3-venv awscli jq -y

echo "Retrieving GitHub token from Secrets Manager"
TOKEN="$(aws secretsmanager get-secret-value \
  --secret-id github-key \
  --query SecretString \
  --output text | jq -r '."github-key"')"

echo "Creating temporary Git credential helper"
ASKPASS="$(mktemp)"
trap 'rm -f "$ASKPASS"; unset TOKEN' EXIT

cat > "$ASKPASS" <<'EOF'
#!/bin/sh
case "$1" in
  *Username*) printf '%s\n' "x-access-token" ;;
  *Password*) printf '%s\n' "$GITHUB_TOKEN" ;;
esac
EOF

chmod 700 "$ASKPASS"

export GITHUB_TOKEN="$TOKEN"
export GIT_ASKPASS="$ASKPASS"
export GIT_TERMINAL_PROMPT=0

echo "Cloning application repository"
git clone https://github.com/Barracoda130/nc-plus-one.git

echo "Changing to application directory"
cd nc-plus-one

echo "Retrieving the database credentials from Secrets Manager"
db_credentials="$(aws secretsmanager get-secret-value \
  --secret-id nc-plus-one/db-credentials \
  --query SecretString \
  --output text)"
export PGPASSWORD="$(echo "$db_credentials" | jq -r '."DB_PASSWORD"')"

DB_NAME="$(echo "$db_credentials" | jq -r '."DB_NAME"')"

DB_USERNAME="$(echo "$db_credentials" | jq -r '."DB_USERNAME"')"

echo "Retrieving jwt secret from Secrets Manager"
JWT_SECRET="$(aws secretsmanager get-secret-value \
  --secret-id nc-plus-one/jwt-secret \
  --query SecretString \
  --output text | jq -r '."JWT_SECRET"')"

export RDSHOST=${DB_HOST}
if [ "$(psql "host=$RDSHOST port=5432 dbname=$DB_NAME user=$DB_USERNAME" \
  -tAc "SELECT NOT EXISTS (
    SELECT 1
    FROM information_schema.tables
    WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
  );")" = "t" ]; then
  echo "No application tables found; seeding the database"
  python3 
else
  echo "Application tables already exist; skipping database seed"
fi

echo "Creating the Python virtual environment"
python3 -m venv venv

echo "Creating the application environment file"
echo "

LOG_LEVEL=debug
DATABASE_HOST=$RDSHOST
DATABASE_NAME=$DB_NAME
DATABASE_USER=$DB_USERNAME
DATABASE_PASSWORD=$PGPASSWORD
JWT_SECRET=$JWT_SECRET
" > .env

echo "Installing application requirements"
sudo make requirements

echo "Running application development setup"
sudo make dev-setup

echo "Redirecting port 80 to port 8000"
sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8000

echo "Starting the application server"
sudo make start-server