FROM node:20-alpine
WORKDIR /workspace/apps/caregiver-web
COPY apps/caregiver-web/package*.json ./
RUN npm install
COPY apps/caregiver-web ./
