import boto3
import random
import time

# config
BUCKET_NAME = 'finops-blackfriday-logs-diogo'
NUM_ARQUIVOS = 1000

s3 = boto3.client('s3')

print(f"Iniciando ataque de logs simulados no bucket: {BUCKET_NAME}...")

for i in range(NUM_ARQUIVOS):
    nome_arquivo = f"logs/server-app-01/access_log_{int(time.time())}_{i}.txt"
    conteudo = f"Timestamp: {time.time()} | Level: INFO | Msg: Transaction started for cart_id_{random.randint(1000,9999)}\n" * 15
    s3.put_object(Bucket=BUCKET_NAME, Key=nome_arquivo, Body=conteudo)
    if i % 100 == 0:
        print(f"✅ {i} arquivos enviados...")

print(f"🚀 Sucesso! {NUM_ARQUIVOS} arquivos pequenos criados. O cenário de desperdício está pronto.")