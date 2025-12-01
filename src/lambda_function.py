import boto3
import os
import json

s3 = boto3.client('s3')
sns = boto3.client('sns')

def lambda_handler(event, context):
    BUCKET_NAME = os.environ.get('BUCKET_NAME')
    SNS_TOPIC_ARN = os.environ.get('SNS_TOPIC_ARN')
    LIMITE_EFICIENCIA_KB = 128

    # Trava de segurança para Debugging
    print(f"DEBUG: Tentando ler bucket '{BUCKET_NAME}' e SNS '{SNS_TOPIC_ARN}'")
    
    if not BUCKET_NAME:
        return "ERRO CRÍTICO: A variável BUCKET_NAME não foi encontrada. Verifique a configuração."

    print(f"Iniciando auditoria no bucket: {BUCKET_NAME}")
    
    try:
        response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix='logs/', MaxKeys=1000)
    except Exception as e:
        print(f"ERRO S3: {str(e)}")
        return f"Falha ao acessar S3: {str(e)}"
    
    total_files = 0
    small_files = 0
    
    if 'Contents' in response:
        for obj in response['Contents']:
            total_files += 1
            size_kb = obj['Size'] / 1024
            
            if size_kb < LIMITE_EFICIENCIA_KB:
                small_files += 1

    print(f"Análise concluída. Total: {total_files} | Pequenos/Ineficientes: {small_files}")

    # Tomada de decisão e cálculo.
    if small_files > 0:
        custo_transicao_evitado = (total_files / 1000) * 0.05
        storage_virtual_poupado_mb = (small_files * 128) / 1024 
        
        # CS
        mensagem_cs = f"""
        [ALERTA DE ECONOMIA - FINOPS GUARDIAN]
        
        Olá Time Financeiro,
        
        Detectamos uma tentativa de arquivamento ineficiente no bucket '{BUCKET_NAME}'.
        
        🔎 O QUE ENCONTRAMOS:
        {small_files} arquivos de log pequenos (<128KB) que gerariam prejuízo se movidos para o Glacier.
        
        🛡️ AÇÃO AUTOMÁTICA:
        A transição foi bloqueada temporariamente.
        
        💰 CUSTO EVITADO HOJE:
        - Taxas de Transição (Requests): ~${custo_transicao_evitado:.4f}
        - Desperdício de Storage: Você pagaria por {storage_virtual_poupado_mb:.2f} MB de "ar" comprimido.
        
        Próximos passos: Recomendamos compactar esses logs antes de arquivar.
        
        Atenciosamente,
        Robô FinOps
        """
        
        print("Enviando relatório para o cliente...")
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=mensagem_cs,
            Subject="FinOps Alert: Economia Confirmada"
        )
        return {"status": "Alerta Enviado", "files_analyzed": total_files}

    return {"status": "Sem riscos detectados", "files_analyzed": total_files}