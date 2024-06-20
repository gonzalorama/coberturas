# Usar una imagen base de Ubuntu
FROM ubuntu:22.04

# Configurar el entorno no interactivo
ENV DEBIAN_FRONTEND=noninteractive

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    git \
    curl \
    wget

# Clonar el repositorio desde GitHub
RUN git clone https://github.com/gonzalorama/coberturas.git /app
WORKDIR /app

RUN cp -Rf src/chainlit/public .
RUN rm .chainlit/config.toml
RUN cp src/chainlit/.chainlit/config.toml .chainlit/

ENV PYTHONPATH "${PYTHONPATH}:/app"
ENV CHROMA_DB_PATH "/app/data/chroma"

# Aceptar el argumento de construcción para la clave de API de OpenAI
ARG OPENAI_API_KEY
ENV OPENAI_API_KEY=${OPENAI_API_KEY}

# Instalar las dependencias de Python
RUN pip3 install -r requirements.txt

# Exponer el puerto solo para la aplicación
EXPOSE 8000

# Configurar el punto de entrada para iniciar la aplicación
CMD ["sh", "-c", "chainlit run src/chainlit/app.py --host 0.0.0.0 --port 8000"]
