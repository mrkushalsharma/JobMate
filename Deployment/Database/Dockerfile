version: '3.8'
services:
  db:
    image: postgres:14.1-alpine
    container_name: 'postgres-db'
    restart: always
    environment:
      POSTGRES_USER: pgadmin
      POSTGRES_PASSWORD: LjDtTR4Z2MwM3dQG
    volumes: 
      - /home/ubuntu/postgres-db:/var/lib/postgresql/data
    ports:
      - "5432:5432"
