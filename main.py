import os
import yaml
from dotenv import load_dotenv

# Importa as fábricas dos nossos componentes modulares
from src.components.loaders import get_loader
from src.components.vector_stores import get_vector_store
from src.components.llms import get_llm

# Importa a classe principal do motor RAG
from src.core.engine import RAGEngine

# Importa utilitários, como logging (opcional, mas boa prática)
# from src.utils.helpers import setup_logging


def load_config(config_path="config.yaml"):
    """Carrega o arquivo de configuração YAML."""
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        print("✔ Configurações carregadas com sucesso de config.yaml")
        return config
    except FileNotFoundError:
        print(f"Erro: O arquivo de configuração '{config_path}' não foi encontrado.")
        exit()
    except yaml.YAMLError as e:
        print(f"Erro ao fazer o parse do arquivo YAML: {e}")
        exit()


def main():
    """
    Ponto de entrada principal da aplicação.
    Orquestra a inicialização e execução do pipeline RAG.
    """
    print("🚀 Iniciando o Agente RAG Modular...")

    # --- 1. Carregamento de Configurações e Variáveis de Ambiente ---
    load_dotenv()
    config = load_config()

    # setup_logging() # Opcional: para um sistema de logs mais robusto

    # --- 2. Instanciação dos Componentes via Fábricas ---
    # O main.py não sabe QUAL componente está sendo usado, apenas pede para as fábricas criarem
    # com base no que está no config.yaml.

    print("🧩 Montando os componentes do pipeline...")

    try:
        # Pega a configuração específica de cada componente
        loader_config = config["loader"]
        vector_store_config = config["vector_store"]
        llm_config = config["llm"]

        # Usa as fábricas para criar as instâncias
        document_loader = get_loader(loader_type=loader_config["type"])
        vector_store = get_vector_store(
            store_type=vector_store_config["type"], config=vector_store_config
        )
        llm = get_llm(provider=llm_config["provider"], config=llm_config)

        print("✔ Componentes instanciados com sucesso!")

    except (ValueError, KeyError) as e:
        print(f"🚨 Erro ao instanciar componentes a partir da configuração: {e}")
        print(
            "Verifique se o seu config.yaml está correto e se os tipos especificados têm implementações."
        )
        exit()

    # --- 3. Injeção de Dependência no Motor RAG ---
    # Criamos a instância do nosso motor e passamos os componentes já prontos para ele.
    rag_engine = RAGEngine(loader=document_loader, vector_store=vector_store, llm=llm)
    print("✔ Motor RAG montado e pronto para operar.")

    # --- 4. Interface Interativa com o Usuário ---
    print("\n=============================================")
    print("  Bem-vindo ao seu Agente de Código!")
    print("=============================================")

    # Verifica se o índice já existe para não precisar indexar tudo sempre
    index_exists = vector_store.check_index()
    if not index_exists:
        print(
            "\nℹ️  Nenhum índice encontrado. É recomendado indexar seus documentos primeiro."
        )
        choice = "1"
    else:
        choice = input(
            "\nO que você gostaria de fazer?\n  [1] Indexar/Re-indexar documentos\n  [2] Fazer uma pergunta ao seu código\nEscolha uma opção: "
        )

    if choice == "1":
        print("\nIniciando processo de indexação...")
        rag_engine.index(
            path=loader_config["path"],
            glob=loader_config["glob"],
            chunk_size=config["text_splitter"]["chunk_size"],
            chunk_overlap=config["text_splitter"]["chunk_overlap"],
        )
        print("\n✅ Indexação concluída com sucesso!")
        print(
            "Agora você pode reiniciar o programa e escolher a opção '2' para fazer perguntas."
        )

    elif choice == "2":
        if not index_exists:
            print("\n❌ Você precisa indexar os documentos antes de fazer perguntas.")
            exit()

        print("\n🤖 Estou pronto para responder. Digite 'sair' para terminar.")
        while True:
            question = input("\nSua pergunta: ")
            if question.lower() == "sair":
                break

            print("\n🔄 Pensando...")
            answer = rag_engine.ask(question)

            print("\n--- Resposta do Agente ---")
            print(answer)
            print("--------------------------")
    else:
        print("Opção inválida. Encerrando.")


if __name__ == "__main__":
    main()
