# E-Fecaf Global - Monitoramento Contínuo de Performance
# 🚀 E-Fecaf Global - Monitoramento Contínuo de Performance

![Status](https://img.shields.io/badge/status-ativo-success)
![Locust](https://img.shields.io/badge/Locust-2.43.4-blue)
![Python](https://img.shields.io/badge/Python-3.14-blue)
![Grafana](https://img.shields.io/badge/Grafana-9.0-orange)

## 📋 Sobre o Projeto

Solução completa de monitoramento contínuo de performance para a E-Fecaf Global, uma empresa de e-commerce em rápida expansão. O projeto visa garantir estabilidade durante picos de tráfego (Black Friday, promoções) através de:

- ✅ Testes de estresse automatizados
- ✅ Monitoramento em tempo real
- ✅ Dashboards visuais
- ✅ Alertas proativos

## 🎯 Problema Resolvido

Durante eventos promocionais, a plataforma enfrentava:
- ⏱️ Lentidão extrema
- 💥 Quedas de sistema
- 😡 Experiência insatisfatória para clientes
- 💸 Perdas financeiras significativas

**Este projeto elimina esses problemas através de monitoramento contínuo e testes preventivos.**

## 🛠️ Tecnologias Utilizadas

| Ferramenta | Função | Versão |
|------------|--------|---------|
| **Locust** | Testes de estresse | 2.43.4 |
| **Python** | Scripts de simulação | 3.14+ |
| **Grafana** | Dashboards e visualização | 9.0+ |
| **Prometheus** | Coleta de métricas | (planejado) |

## 📁 Estrutura do Projeto

E-Fecaf Global/
├── locustfile.py # Script principal de teste de carga
├── teste_real.py # Testes com API real
├── dashboard-efecaf.json # Dashboard Grafana (importar)
├── requirements.txt # Dependências Python
├── README.md # Este arquivo
└── relatorios/ # Pasta para relatórios gerados


## 🚀 Como Executar

### 1️⃣ Instalar Dependências

```bash
# Instalar Locust
pip install locust

# Verificar instalação
locust --version

2️⃣ Executar Teste de Carga
Modo Web (Recomendado para desenvolvimento)
bash
locust -f locustfile.py --host=https://jsonplaceholder.typicode.com
Acesse: http://localhost:8089

Modo Headless (Para CI/CD)
bash
locust -f locustfile.py --host=https://jsonplaceholder.typicode.com --headless -u 100 -r 10 --run-time 5m

Gerar Relatório HTML
bash
locust -f locustfile.py --host=https://jsonplaceholder.typicode.com --headless -u 500 -r 50 --run-time 5m --html=relatorio_performance.html

3️⃣ Configurar Grafana

bash
# Baixar e instalar Grafana
# Acesse: https://grafana.com/grafana/download

# Após instalação, acesse:
http://localhost:3000
# Login: admin / admin

# Importar dashboard:
# Dashboards → Import → Paste JSON (dashboard-efecaf.json)

4️⃣ Testar com Site Real

bash
# Para testar o site da E-Fecaf Global (quando disponível)
locust -f locustfile.py --host=https://e-fecaf-global.com.br

# Para ambiente de staging
locust -f locustfile.py --host=https://staging.e-fecaf-global.com.br

📊 Cenários de Teste
O locustfile.py simula 4 cenários reais de usuário:

Cenário	           Peso	    Descrição
Navegação	        5x	    Busca produtos e visualização
Adicionar carrinho	3x	    Adiciona produtos ao carrinho
Visualizar carrinho	2x	    onsulta carrinho atual
Checkout	        1x	    Finaliza compra completa

📈 Métricas Monitoradas

⏱️ Tempo de resposta (p50, p95, p99)

❌ Taxa de erro (4xx, 5xx)

🚦 Requisições por segundo (RPS)

💻 Uso de CPU/Memória

🔄 Latência por endpoint

🎨 Dashboards Disponíveis
O dashboard Grafana inclui:

Visão Executiva - Saúde geral da plataforma

Visão Técnica - Métricas detalhadas por endpoint

Visão de Pico - Monitoramento durante eventos

🔔 Configuração de Alertas

Alertas automáticos configurados:

Alerta	            Condição	        Ação
Latência alta	    p95 > 2s por 2min	Notificar Slack
Taxa de erro	    > 1% por 1min	    Acionar PagerDuty
Indisponibilidade	API offline	        Chamada SMS

🧪 Exemplo de Uso

Teste Rápido (30 segundos)
bash
locust -f locustfile.py --host=https://jsonplaceholder.typicode.com --headless -u 10 -r 2 --run-time 30s

Teste de Pico (1000 usuários)
bash
locust -f locustfile.py --host=https://jsonplaceholder.typicode.com --headless -u 1000 -r 100 --run-time 10m --html=teste_pico.html

Teste de Resistência (1 hora)
bash
locust -f locustfile.py --host=https://jsonplaceholder.typicode.com --headless -u 500 -r 20 --run-time 1h --csv=resultados_1hora

📦 Requirements.txt
txt

locust>=2.20.0
requests>=2.32.0

Instalar com:

bash
pip install -r requirements.txt

🐛 Solução de Problemas

Erro: "ModuleNotFoundError: No module named locust"
bash
pip install locust

Erro: "Address already in use" (porta 8089 ocupada)
bash
locust -f locustfile.py --host=URL --web-port 8090

Dashboard Grafana mostra "No Data"
Verifique se o Prometheus está rodando

Ou use "TestData DB" como fonte de dados temporária

📈 Resultados Esperados
Com a implementação completa:

Métrica	                    Antes	    Depois
Disponibilidade	            95%	        99.9%
Tempo resposta	            4-5s	    < 1s
Incidentes por mês	        5-7	        < 1
Perda financeira (evento)	R$1.2M	    R$0

🔄 Melhorias Contínuas Baseadas em Métricas
Cache Redis para produtos mais acessados

Auto-scaling horizontal baseado em CPU/latência

Read replicas para banco de dados

CDN para assets estáticos

Rate limiting por IP
