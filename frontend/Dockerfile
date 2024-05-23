# Use the official image as a parent image
FROM node:14

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Copy the environment file
COPY .env /app/.env

# Install any needed packages
RUN npm install

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Run npm run serve when the container launches
CMD ["npm", "run", "serve"]
