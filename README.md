# 🛡️ AWS S3 FinOps Guardian

![AWS](https://img.shields.io/badge/AWS-Level%20Up-232F3E?style=flat&logo=amazon-aws)
![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=flat&logo=python)
![Status](https://img.shields.io/badge/Status-Completed-success)
![Focus](https://img.shields.io/badge/Focus-FinOps%20%26%20Cost%20Avoidance-green)

> **Uma automação serverless que atua como "Guarda-Costas Financeiro",
> prevenindo custos ocultos de armazenamento e transição de dados no
> Amazon S3.**

---

## 📸 Visão Geral do Projeto

![Relatório de Economia](img/relatorio-economia.png)

Este projeto simula um cenário pós-Black Friday onde milhões de logs
pequenos são gerados. O objetivo é demonstrar como uma política de
_Lifecycle_ mal configurada pode transformar uma conta de **\$0.46** em
um prejuízo de **\$500+**, e como a automação pode evitar isso
proativamente.

---

## ⚠️ O Problema (A "Armadilha" do S3)

Mover arquivos para classes de armazenamento mais frias (como _Glacier_
ou _Deep Archive_) nem sempre gera economia. Existem duas taxas ocultas
que afetam arquivos pequenos:

1.  **Taxa de Transição:** A AWS cobra por requisição (PUT/Transition).
    Mover 10 milhões de arquivos custa caro.
2.  **Mínimo de Objeto (128KB):** Arquivos menores que 128KB são
    cobrados como se tivessem 128KB nessas classes.

**O Cenário:** 10 Milhões de logs de 2KB cada.\
\* **Tamanho Real:** 20 GB\
\* **Tamanho Cobrado no Glacier:** 1.2 TB (Inflação de 60x no custo)

---

## 🏗️ Arquitetura da Solução

A solução utiliza uma abordagem 100% Serverless para auditar, calcular e
notificar.

![Arquitetura](img/arquitetura.png)

1.  **Gatilho (EventBridge):** Um Cron Job executa a auditoria
    semanalmente.\
2.  **Cérebro (AWS Lambda + Python):**
    -   Lista e analisa amostragem de objetos no S3.
    -   Calcula o tamanho médio e a viabilidade financeira.
    -   Decide se o arquivamento gera ROI ou prejuízo.
3.  **Comunicação (Amazon SNS):** Envia um alerta traduzindo o risco
    técnico em valor monetário economizado.

---

## 💰 Comparativo de Custos (Simulação)

Baseado em um bucket com **10 Milhões de objetos** pequenos:

---

Estratégia Custo de Taxas de Multa de **Custo Total
Armazenamento Transição Retenção Est.**
(\<180 dias)

---

**S3 Standard** \~\$0.46 \$0.00 \$0.00 **\$0.46**

**Glacier Deep \~\$1.24 \$500.00 \~\$6.20 **🔴
Archive \~\$507.44**
(Errado)**

**FinOps \~\$0.46 \$0.00 \$0.00 **🟢 \$0.46**
Guardian  
 (Automação)**

---

> **Resultado:** A automação evitou desperdício de mais de **\$500
> dólares** em um único mês.

---

## 🚀 Como Executar

### Pré-requisitos

-   Conta AWS ativa.\
-   Python 3.x e Boto3 instalados.\
-   AWS CLI configurado.

### Passo 1: Configuração do Ambiente

```bash
git clone https://github.com/diogomsk/aws-finops-s3-guardian.git
cd aws-finops-s3-guardian
pip install boto3
```

### Passo 2: Gerar o Caos (Simulação)

```bash
python src/gerador_caos.py
```

### Passo 3: Deploy da Lambda

1.  Crie uma função Lambda com Python 3.13.\
2.  Cole o código de `src/lambda_function.py`.\
3.  Configure as variáveis de ambiente:
    -   `BUCKET_NAME`
    -   `SNS_TOPIC_ARN`

---

## 🛠️ Tecnologias Utilizadas

-   **AWS Lambda**\
-   **Amazon S3**\
-   **Amazon SNS**\
-   **Amazon EventBridge**\
-   **Python (Boto3)**\
-   **IAM (Least Privilege)**

---

## 👨‍💻 Autor

**Diogo P. Maske**\
Cloud Computing \| DevOps \| Customer Success
