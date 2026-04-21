FROM node:22-alpine

WORKDIR /app

# Install pnpm
RUN npm install -g pnpm

# Copy dependency files first (layer caching)
COPY package.json pnpm-lock.yaml ./

RUN pnpm install

# Copy the rest of the source code
COPY . .

EXPOSE 5173

CMD ["pnpm", "dev", "--host", "0.0.0.0"]
