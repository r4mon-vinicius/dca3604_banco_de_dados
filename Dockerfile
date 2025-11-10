# 1. Imagem base
FROM python:3.10-slim

# 2. Define o diretório de trabalho
WORKDIR /app

# 3. Copia APENAS o arquivo de requisitos
COPY requirements.txt .

# 4. Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copia o código-fonte (src)
COPY ./src .

# 6. Copia os dados CSV (NOVO)
COPY ./csv ./csv

# 7. Copia e dá permissão ao script de entrada (NOVO)
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

# 8. Expõe a porta do Streamlit
EXPOSE 8501

# 9. Define o script de entrada como o comando principal (NOVO)
ENTRYPOINT ["./entrypoint.sh"]

# (O CMD anterior foi removido e substituído pelo ENTRYPOINT)