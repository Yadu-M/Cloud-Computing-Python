# Build the frontend
FROM node:18-bullseye-slim AS build-frontend

WORKDIR /app

# Copy package files for frontend
COPY package*.json ./

# Install frontend dependencies
RUN npm ci

# Copy the frontend code
COPY . .

# Build the frontend
RUN npm run build

# Build the backend
FROM python:3.9-slim AS build-backend

WORKDIR /app

# Copy the backend code
COPY server/ .

# Install backend dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Final image
FROM python:3.9-slim

WORKDIR /app

# Copy the built frontend from the first stage
COPY --from=build-frontend /app/dist ./frontend/dist

# Copy the backend code and dependencies from the second stage
COPY --from=build-backend /app .

# Install backend dependencies for the final image
COPY --from=build-backend /app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port for the backend server
EXPOSE 8000

# Set the command to start the backend server and serve the frontend
CMD ["uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]