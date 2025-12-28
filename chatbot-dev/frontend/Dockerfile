FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
RUN npm install terser -D
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]