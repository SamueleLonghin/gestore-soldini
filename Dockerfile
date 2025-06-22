FROM python:3.12

# Installa git (necessario per il clone)
RUN apt-get update && apt-get install -y git && apt-get clean

# Crea la directory dell'app
WORKDIR /app

# Clona la repo (puoi usare anche HTTPS con accesso pubblico)
# RUN git clone https://github.com/SamueleLonghin/gestore-soldini .
COPY . .

# Installa le dipendenze
RUN pip install --no-cache-dir -r requirements.txt

# Espone la porta di Flask
EXPOSE 5000

# Comando di default
CMD ["flask", "run", "--host=0.0.0.0 "]
