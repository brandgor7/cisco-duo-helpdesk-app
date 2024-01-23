# Frontend/Dockerfile
# Use an official Node runtime as a parent image
FROM node:latest

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy package.json and package-lock.json
COPY package*.json ./

# Try a clean install
RUN npm ci

# Bundle app source
COPY . .

# Your app binds to port 5173, so use the EXPOSE instruction
EXPOSE 5173

# Define environment variable
ENV NODE_ENV development

# Run npm run dev when the container launches
CMD ["npm", "run", "dev"]
