#!/bin/sh

# Navigate to the frontend directory
cd frontend

# Install frontend dependencies
npm install

# Build the frontend
npm run build

# Move the build files to the backend's static folder
mkdir -p ../backend/static
cp -r dist/* ../backend/static

# Navigate back to the root directory
cd ..