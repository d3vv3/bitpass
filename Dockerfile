FROM python:3.7.7-alpine3.10

WORKDIR /

COPY . .

# Install nodejs, npm and gpg
RUN apk add nodejs npm gnupg build-base linux-headers

# Install gpg for python
RUN pip install 'gnupg==2.3.1'

# Install bitwarden-cli
RUN npm install -g @bitwarden/cli@1.9.0

# ENVIROMENT VARIABLES
ENV BW_USER <your_email>
ENV BW_PASSWORD <your_password>
ENV PUBLIC_GPG <your_public_key.pub>

# Run the script
CMD ["python", "./main.py"]
