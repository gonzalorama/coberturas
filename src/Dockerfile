# Usar una imagen base de Ubuntu
FROM ubuntu:20.04

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

# Instalar las dependencias de Python
RUN pip3 install -r requirements.txt

# Descargar y descomprimir ChromaDB
RUN wget https://github.com/chroma-db/chroma/releases/download/v0.0.1/chromadb-linux-amd64.tar.gz
RUN tar -xvzf chromadb-linux-amd64.tar.gz -C /usr/local/bin

# Exponer el puerto solo para la aplicación
EXPOSE 8501

# Configurar el punto de entrada para iniciar ChromaDB y la aplicación
CMD ["sh", "-c", "/usr/local/bin/chromadb --host 127.0.0.1 --port 8000 & chainlit run src/chainlit/app.py --host 0.0.0.0 --port 8501"]
