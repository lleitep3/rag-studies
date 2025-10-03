"""
Exemplo para testar o Code Review
"""


def calculate_sum(a, b):
    # Função simples para testar o revisor
    # Propositalmente sem type hints e documentação adequada
    return a + b


def process_data(data):
    # Função com problemas de segurança e performance
    result = []
    for item in data:
        # Usa eval sem validação
        processed = eval(item)
        result.append(processed)
    return result


class UserManager:
    def __init__(self):
        self.users = {}

    def add_user(self, username, password):
        # Armazena senha em texto plano
        self.users[username] = password

    def authenticate(self, username, password):
        # Comparação insegura
        return self.users.get(username) == password
