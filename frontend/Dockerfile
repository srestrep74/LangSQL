FROM node:20-alpine AS build

# Workdir
WORKDIR /app

# Necessary for the build
COPY package*.json ./

# Dependencies
RUN npm install

# Copy the rest of the code
COPY . .

# Build the app
RUN npm run build-only

FROM nginx:stable-alpine AS production

# Cpy the generated files
COPY --from=build /app/dist /usr/share/nginx/html

# Copy the nginx configuration file
COPY nginx.conf /etc/nginx/nginx.conf

# Expose the port the app runs on
EXPOSE 80

# Default nginx.conf
CMD ["nginx", "-g", "daemon off;"]