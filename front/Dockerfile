# Base Image 
FROM nginx:alpine

COPY /html /usr/share/nginx/html/
COPY /css /usr/share/nginx/html/css/
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]