## Build Stage
#FROM node:18-alpine AS build
#WORKDIR /app
#COPY package*.json ./
#RUN npm install
#COPY . .
#ARG VITE_API_URL
#ENV VITE_API_URL=$VITE_API_URL
#RUN npm run build
#
## Production Stage
#FROM nginx:stable-alpine AS production
#COPY --from=build /app/dist /usr/share/nginx/html
#EXPOSE 80
#CMD ["nginx", "-g", "daemon off;"]

# Use an official Nginx image as the base
FROM nginx:alpine

# Set the working directory
WORKDIR /usr/share/nginx/html

# Remove the default Nginx static assets
RUN rm -rf ./*

# Copy built React files from local ./dist to Nginx public directory
COPY ./dist .

# Copy a custom Nginx config if you have one (optional)
# COPY nginx.conf /etc/nginx/nginx.conf

# Expose port 80
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]