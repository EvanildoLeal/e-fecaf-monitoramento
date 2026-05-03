"""
locustfile.py - Teste de Carga para E-Fecaf Global
Monitoramento com Prometheus + Grafana
"""

from locust import HttpUser, task, between, events
import random
import logging
from datetime import datetime
from prometheus_client import start_http_server, Counter, Histogram, Gauge
import threading

# ============================================
# CONFIGURAÇÃO
# ============================================
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ============================================
# MÉTRICAS PROMETHEUS
# ============================================
REQUESTS_TOTAL = Counter('locust_requests_total', 'Total de requisições', ['method', 'endpoint', 'status'])
REQUEST_DURATION = Histogram('locust_request_duration_seconds', 'Duração das requisições', ['method', 'endpoint'])
ACTIVE_USERS = Gauge('locust_active_users', 'Usuários ativos')
ERROR_RATE = Gauge('locust_error_rate', 'Taxa de erro percentual')

# ============================================
# SERVIDOR PROMETHEUS
# ============================================
def start_metrics_server():
    start_http_server(8000)
    print("\n" + "="*50)
    print("✅ Servidor Prometheus rodando em http://localhost:8000/metrics")
    print("="*50 + "\n")

threading.Thread(target=start_metrics_server, daemon=True).start()

# ============================================
# ESTATÍSTICAS
# ============================================
class TestStats:
    def __init__(self):
        self.total_requests = 0
        self.total_errors = 0
    
    def add_request(self, success=True):
        self.total_requests += 1
        if not success:
            self.total_errors += 1
        if self.total_requests > 0:
            ERROR_RATE.set((self.total_errors / self.total_requests) * 100)

stats = TestStats()

# ============================================
# USUÁRIO SIMULADO
# ============================================
class EcommerceUser(HttpUser):
    wait_time = between(1, 5)
    
    PRODUTOS = [
        {"id": 101, "nome": "Café Especial", "preco": 49.90},
        {"id": 102, "nome": "Kit Chá Premium", "preco": 89.90},
        {"id": 103, "nome": "Cafeteira Elétrica", "preco": 299.90},
        {"id": 104, "nome": "Grãos Gourmet", "preco": 35.90},
    ]
    
    def on_start(self):
        ACTIVE_USERS.inc()
        self.carrinho = []
        self.client.get("/", name="01_homepage")
        self.client.get("/categoria/cafes", name="02_categorias")
    
    def on_stop(self):
        ACTIVE_USERS.dec()
    
    @task(5)
    def browse_products(self):
        termos = ["café", "chá", "kit", "presente"]
        termo = random.choice(termos)
        with self.client.get(f"/buscar?q={termo}", name="03_busca_produtos", catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Busca falhou: {response.status_code}")
        
        produto = random.choice(self.PRODUTOS)
        self.client.get(f"/produto/{produto['id']}", name="04_detalhe_produto")
    
    @task(3)
    def add_to_cart(self):
        produto = random.choice(self.PRODUTOS)
        quantidade = random.randint(1, 3)
        with self.client.post("/carrinho/adicionar", name="05_adicionar_carrinho", 
                              json={"produto_id": produto["id"], "quantidade": quantidade}, catch_response=True) as response:
            if response.status_code == 200:
                self.carrinho.append({"produto": produto, "quantidade": quantidade})
                response.success()
            else:
                response.failure(f"Falha: {response.status_code}")
    
    @task(2)
    def view_cart(self):
        self.client.get("/carrinho", name="06_visualizar_carrinho")
    
    @task(1)
    def checkout(self):
        if len(self.carrinho) == 0:
            return
        
        total = sum(item["produto"]["preco"] * item["quantidade"] for item in self.carrinho)
        
        pagamento = {
            "cliente": {"nome": "Cliente Teste", "email": "teste@email.com"},
            "itens": [{"produto_id": item["produto"]["id"], "quantidade": item["quantidade"]} for item in self.carrinho],
            "total": total
        }
        
        with self.client.post("/checkout/pagar", name="07_finalizar_compra", json=pagamento, catch_response=True) as response:
            if response.status_code == 200:
                logger.info(f"✅ Compra finalizada! R$ {total:.2f}")
                self.carrinho = []
                stats.add_request(success=True)
                response.success()
            else:
                stats.add_request(success=False)
                response.failure(f"Pagamento falhou: {response.status_code}")

# ============================================
# EVENTOS
# ============================================
@events.request.add_listener
def on_request_listener(request_type, name, response_time, response_length, response, context, exception, **kwargs):
    status = 'error' if exception else 'success'
    REQUESTS_TOTAL.labels(method=request_type, endpoint=name, status=status).inc()
    
    if not exception:
        REQUEST_DURATION.labels(method=request_type, endpoint=name).observe(response_time / 1000.0)
        stats.add_request(success=True)
    else:
        stats.add_request(success=False)
    
    if response_time > 3000:
        logger.warning(f"⚠️ Requisição lenta: {name} - {response_time}ms")

@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    print("\n" + "🔥"*30)
    print("🔥 TESTE DE CARGA INICIADO")
    print("🔥 Grafana: http://localhost:3000")
    print("🔥 Métricas: http://localhost:8000/metrics")
    print("🔥"*30 + "\n")

# ============================================
if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════╗
    ║  E-FECAF GLOBAL - Teste de Carga         ║
    ║  Prometheus: http://localhost:8000/metrics║
    ║  Locust Web: http://localhost:8089       ║
    ║  Grafana: http://localhost:3000          ║
    ╚══════════════════════════════════════════╝
    """)