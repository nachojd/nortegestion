FROM node:18-alpine

WORKDIR /app

# Instalar dependencias
COPY package*.json ./
RUN npm config set registry https://registry.npmjs.org/ && \
    npm install --production

# Copiar código fuente
COPY . .

# Build para producción
RUN npm run build

# Exponer puerto
EXPOSE 3000

# Variables de entorno
ENV NODE_ENV=production

# Comando de inicio
CMD ["npm", "start"]