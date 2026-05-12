FROM python:3.12-slim

# Python test runner
RUN pip install --no-cache-dir pytest

# Node.js + Go for TypeScript and Go support
RUN apt-get update && apt-get install -y nodejs npm golang-go && rm -rf /var/lib/apt/lists/*

# Pre-install vitest in a shared runner directory
WORKDIR /runner
COPY package.json .
RUN npm install

WORKDIR /
