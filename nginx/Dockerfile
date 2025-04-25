# Use official Nginx image
FROM nginx:latest

# copy configuration Nginx into container
COPY nginx.conf /etc/nginx/nginx.conf

# copy static files of our app in service directory
COPY staticfiles/ /usr/share/nginx/html/

# Open port 80 for HTTP requests
EXPOSE 80