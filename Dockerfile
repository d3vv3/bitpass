FROM python:3.9.2-slim-buster

RUN mkdir /app /password-store /gpg_home

WORKDIR /app

COPY . .

# Install nodejs, npm and gpg
RUN apt update
RUN apt install nodejs npm gnupg -y

# Install gpg for python
RUN pip install -r requirements.txt

# Install bitwarden-cli
RUN npm install -g @bitwarden/cli@1.9.0

# ENVIROMENT VARIABLES
# ENV BW_USER <your_email>
# ENV BW_PASSWORD <your_password>
# ENV PUBLIC_GPG <your_public_key.pub>
# ENV NOTIF_URL <your_url> for apprise here https://github.com/caronc/apprise

# Run the script
CMD ["python", "main.py"]
