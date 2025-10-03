#!/usr/bin/env python3
"""
🛠️ RAG App Generator
====================

Script para criar a estrutura básica de um novo app no projeto RAG Study.
Gera automaticamente todos os arquivos necessários com uma estrutura padrão.
"""

import os
import sys
import argparse
from pathlib import Path
from datetime import datetime
from typing import Optional

# Adiciona src ao path para usar ColoredOutput
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.helpers.colored_output import ColoredOutput


class AppGenerator:
    """Gerador de estrutura de apps RAG"""
    
    def __init__(self, app_name: str, app_type: str = "basic", author: str = "RAG Team"):
        """
        Inicializa o gerador.
        
        Args:
            app_name: Nome do app (será usado como nome da pasta)
            app_type: Tipo de app (basic, chat, analysis, api)
            author: Nome do autor
        """
        self.app_name = app_name.lower().replace(" ", "-")
        self.app_title = " ".join(word.capitalize() for word in app_name.replace("-", " ").split())
        self.app_type = app_type
        self.author = author
        self.date = datetime.now().strftime("%Y-%m-%d")
        self.app_dir = project_root / "apps" / self.app_name
    
    def create_directory_structure(self) -> bool:
        """Cria a estrutura de diretórios do app"""
        if self.app_dir.exists():
            ColoredOutput.error(f"App '{self.app_name}' já existe em {self.app_dir}")
            return False
        
        try:
            self.app_dir.mkdir(parents=True, exist_ok=True)
            ColoredOutput.success(f"Diretório criado: {self.app_dir}")
            return True
        except Exception as e:
            ColoredOutput.error(f"Erro ao criar diretório: {e}")
            return False
    
    def generate_main_py(self) -> str:
        """Gera o conteúdo do arquivo main.py"""
        template = '''#!/usr/bin/env python3
"""
{emoji} {title}
{separator}

{description}

Criado em: {date}
Autor: {author}
"""

import sys
import os
import argparse
from pathlib import Path
from typing import Optional, Dict, Any

# Adiciona src ao path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from src.helpers.colored_output import ColoredOutput
from src.core.engine import create_rag_engine


class {class_name}:
    """Classe principal do {title}"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Inicializa o {title}.
        
        Args:
            config: Configurações opcionais do app
        """
        self.config = config or {{}}
        self.engine = None
        self.is_initialized = False
        
        ColoredOutput.header("{title}")
        ColoredOutput.info(f"Versão: 1.0.0")
        ColoredOutput.info(f"Tipo: {app_type}")
    
    def setup(self) -> bool:
        """Configura o ambiente e inicializa o engine RAG"""
        try:
            ColoredOutput.info("Inicializando sistema RAG...")
            
            # Cria o engine RAG
            self.engine = create_rag_engine(
                loader_type=self.config.get("loader_type", "python"),
                vector_store_type=self.config.get("vector_store_type", "chroma"),
                llm_type=self.config.get("llm_type", "ollama"),
                llm_kwargs={{"model_name": self.config.get("model_name", "llama3.2:1b")}}
            )
            
            # Indexa dados se necessário
            if self.config.get("index_path"):
                stats = self.engine.setup_pipeline(
                    self.config["index_path"],
                    self.config.get("glob_pattern", "**/*.py")
                )
                ColoredOutput.success(f"Indexados {{stats['documents_loaded']}} documentos")
            
            self.is_initialized = True
            ColoredOutput.success("Sistema inicializado com sucesso!")
            return True
            
        except Exception as e:
            ColoredOutput.error(f"Erro na inicialização: {{e}}")
            return False
    
    def run(self) -> int:
        """Executa a lógica principal do app"""
        if not self.is_initialized:
            if not self.setup():
                return 1
        
        try:
            ColoredOutput.section(
                "Executando {title}",
                "Este é um template básico. Customize este método para implementar sua lógica."
            )
            
            {run_logic}
            
            return 0
            
        except KeyboardInterrupt:
            ColoredOutput.warning("\\nInterrompido pelo usuário")
            return 0
        except Exception as e:
            ColoredOutput.error(f"Erro durante execução: {{e}}")
            return 1
    
    def cleanup(self):
        """Limpa recursos antes de sair"""
        if self.engine:
            ColoredOutput.info("Limpando recursos...")
            # Adicione lógica de limpeza aqui se necessário
            
        ColoredOutput.success("Até logo! 👋")


def parse_arguments():
    """Processa argumentos da linha de comando"""
    parser = argparse.ArgumentParser(
        description="{title} - {description}",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "--config",
        type=str,
        help="Arquivo de configuração JSON (opcional)"
    )
    
    parser.add_argument(
        "--index-path",
        type=str,
        help="Caminho para indexar documentos"
    )
    
    parser.add_argument(
        "--model",
        type=str,
        default="llama3.2:1b",
        help="Modelo LLM a usar (default: llama3.2:1b)"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Modo verboso"
    )
    
    return parser.parse_args()


def load_config(args) -> Dict[str, Any]:
    """Carrega configuração dos argumentos ou arquivo"""
    config = {{}}
    
    # Se um arquivo de config foi especificado
    if args.config:
        import json
        try:
            with open(args.config, 'r') as f:
                config = json.load(f)
            ColoredOutput.success(f"Configuração carregada de {{args.config}}")
        except Exception as e:
            ColoredOutput.warning(f"Erro ao carregar config: {{e}}")
    
    # Sobrescreve com argumentos da linha de comando
    if args.index_path:
        config["index_path"] = args.index_path
    if args.model:
        config["model_name"] = args.model
    config["verbose"] = args.verbose
    
    return config


def main():
    """Função principal"""
    args = parse_arguments()
    config = load_config(args)
    
    app = {class_name}(config)
    return app.run()


if __name__ == "__main__":
    sys.exit(main())
'''
        
        # Customizações baseadas no tipo
        emoji = "🚀"
        description = f"Aplicação RAG do tipo {self.app_type}"
        run_logic = ""
        
        if self.app_type == "chat":
            emoji = "💬"
            description = "Aplicação de chat interativo com RAG"
            run_logic = '''# Loop de chat
            ColoredOutput.info("Digite 'sair' para encerrar\\n")
            
            while True:
                user_input = input("\\n👤 Você: ").strip()
                
                if user_input.lower() in ['sair', 'exit', 'quit']:
                    break
                
                if not user_input:
                    continue
                
                # Processa com RAG
                ColoredOutput.info("Processando...")
                result = self.engine.ask(user_input) if self.engine else {"answer": "Engine não inicializado"}
                
                # Exibe resposta
                ColoredOutput.answer(f"\\n{result['answer']}")'''
        
        elif self.app_type == "analysis":
            emoji = "📊"
            description = "Aplicação de análise de dados com RAG"
            run_logic = '''# Análise de dados
            ColoredOutput.info("Iniciando análise...")
            
            # TODO: Implementar lógica de análise
            ColoredOutput.progress(50, 100, "Análise")
            
            ColoredOutput.section(
                "Resultados",
                "Implemente aqui a lógica de análise específica"
            )'''
        
        elif self.app_type == "api":
            emoji = "🌐"
            description = "API REST com capacidades RAG"
            run_logic = '''# API setup
            ColoredOutput.info("API endpoint seria configurado aqui")
            ColoredOutput.warning("Este é um template - implemente FastAPI ou Flask")
            
            # Exemplo de endpoint simulado
            ColoredOutput.table_row("Endpoint", "Método", "Descrição", widths=[20, 10, 30])
            ColoredOutput.table_row("-"*20, "-"*10, "-"*30, widths=[20, 10, 30])
            ColoredOutput.table_row("/ask", "POST", "Fazer pergunta ao RAG", widths=[20, 10, 30])
            ColoredOutput.table_row("/index", "POST", "Indexar novos documentos", widths=[20, 10, 30])'''
        
        else:  # basic
            emoji = "🎯"
            run_logic = '''# Exemplo básico
            if self.engine:
                question = "O que é RAG?"
                ColoredOutput.question(f"Pergunta: {question}")
                
                result = self.engine.ask(question)
                ColoredOutput.answer(f"Resposta: {result.get('answer', 'Sem resposta')}")
            else:
                ColoredOutput.warning("Engine não inicializado - implemente sua lógica aqui")'''
        
        class_name = "".join(word.capitalize() for word in self.app_name.split("-")) + "App"
        
        return template.format(
            emoji=emoji,
            title=self.app_title,
            separator="=" * (len(self.app_title) + 3),
            description=description,
            date=self.date,
            author=self.author,
            class_name=class_name,
            app_type=self.app_type,
            run_logic=run_logic
        )
    
    def generate_readme(self) -> str:
        """Gera o conteúdo do README.md"""
        emoji_map = {
            "chat": "💬",
            "analysis": "📊",
            "api": "🌐",
            "basic": "🎯"
        }
        
        template = '''# {emoji} {title}

> **{description}**

## 📋 Sobre

Este app foi gerado automaticamente em {date} usando o RAG App Generator.
É um template do tipo **{app_type}** pronto para ser customizado.

## 🚀 Como Usar

### Instalação
```bash
# Navegue para a pasta do app
cd apps/{app_name}

# Instale as dependências (se necessário)
pip install -r requirements.txt
```

### Execução Básica
```bash
python main.py
```

### Com Parâmetros
```bash
# Indexar documentos
python main.py --index-path ../../src --model llama3.2:1b

# Modo verboso
python main.py --verbose

# Com arquivo de configuração
python main.py --config config.json
```

## ⚙️ Configuração

Crie um arquivo `config.json` (opcional):
```json
{{
    "loader_type": "python",
    "vector_store_type": "chroma",
    "llm_type": "ollama",
    "model_name": "llama3.2:1b",
    "index_path": "../../src",
    "glob_pattern": "**/*.py",
    "verbose": true
}}
```

## 🏗️ Estrutura

```
{app_name}/
├── main.py              # Script principal
├── README.md           # Esta documentação
├── requirements.txt    # Dependências Python
└── config.json        # Configuração (opcional)
```

## 🎯 Funcionalidades

{features}

## 🔧 Customização

Para customizar este app:

1. **Modifique `main.py`**:
   - Método `run()` - Implementar lógica principal
   - Método `setup()` - Configurar inicialização
   - Adicionar novos métodos conforme necessário

2. **Adicione novos módulos**:
   - Crie arquivos Python adicionais
   - Importe no `main.py`

3. **Atualize dependências**:
   - Adicione pacotes necessários em `requirements.txt`

## 📝 TODO

- [ ] Implementar lógica específica do app
- [ ] Adicionar tratamento de erros robusto
- [ ] Criar testes unitários
- [ ] Adicionar logging
- [ ] Documentar APIs/interfaces

## 🤝 Contribuindo

Para contribuir com este app:
1. Implemente as funcionalidades pendentes
2. Adicione testes
3. Atualize a documentação
4. Faça um PR

## 📄 Licença

Parte do projeto RAG Study - {author}

---

**Criado em:** {date}  
**Tipo:** {app_type}  
**Versão:** 1.0.0
'''
        
        features = {
            "chat": """- ✅ Chat interativo com RAG
- ✅ Histórico de conversas
- ✅ Comandos especiais
- 🔄 Contexto persistente (TODO)
- 🔄 Export de conversas (TODO)""",
            
            "analysis": """- ✅ Análise de documentos
- ✅ Extração de insights
- ✅ Relatórios formatados
- 🔄 Visualizações (TODO)
- 🔄 Export para PDF/HTML (TODO)""",
            
            "api": """- ✅ Endpoints REST
- ✅ Autenticação básica
- ✅ Rate limiting
- 🔄 WebSocket support (TODO)
- 🔄 GraphQL interface (TODO)""",
            
            "basic": """- ✅ Template básico funcional
- ✅ Integração com RAG Engine
- ✅ Output colorido
- 🔄 Funcionalidades específicas (TODO)
- 🔄 Configuração avançada (TODO)"""
        }
        
        return template.format(
            emoji=emoji_map.get(self.app_type, "🎯"),
            title=self.app_title,
            description=f"Aplicação RAG do tipo {self.app_type}",
            date=self.date,
            app_type=self.app_type,
            app_name=self.app_name,
            features=features.get(self.app_type, features["basic"]),
            author=self.author
        )
    
    def generate_requirements(self) -> str:
        """Gera o conteúdo do requirements.txt"""
        base_requirements = [
            "# Dependências básicas do app",
            "# Gerado automaticamente - adicione conforme necessário",
            "",
            "# Interface e formatação",
            "rich>=13.0.0",
            "colorama>=0.4.6",
            "",
            "# Configuração",
            "python-dotenv>=1.0.0",
            "pydantic>=2.0.0",
        ]
        
        # Adiciona dependências específicas por tipo
        if self.app_type == "chat":
            base_requirements.extend([
                "",
                "# Chat específico",
                "prompt-toolkit>=3.0.0",
            ])
        elif self.app_type == "analysis":
            base_requirements.extend([
                "",
                "# Análise específica",
                "pandas>=2.0.0",
                "matplotlib>=3.5.0",
            ])
        elif self.app_type == "api":
            base_requirements.extend([
                "",
                "# API específica",
                "fastapi>=0.100.0",
                "uvicorn>=0.23.0",
                "httpx>=0.24.0",
            ])
        
        return "\n".join(base_requirements)
    
    def generate_config_example(self) -> str:
        """Gera exemplo de configuração JSON"""
        config = {
            "app_name": self.app_name,
            "app_type": self.app_type,
            "version": "1.0.0",
            "loader_type": "python",
            "vector_store_type": "chroma",
            "llm_type": "ollama",
            "model_name": "llama3.2:1b",
            "index_path": "../../src",
            "glob_pattern": "**/*.py",
            "verbose": False,
            "settings": {
                "temperature": 0.7,
                "max_tokens": 2000,
                "chunk_size": 1000,
                "chunk_overlap": 200
            }
        }
        
        import json
        return json.dumps(config, indent=2)
    
    def create_files(self) -> bool:
        """Cria todos os arquivos do app"""
        files = {
            "main.py": self.generate_main_py(),
            "README.md": self.generate_readme(),
            "requirements.txt": self.generate_requirements(),
            "config.example.json": self.generate_config_example(),
        }
        
        try:
            for filename, content in files.items():
                file_path = self.app_dir / filename
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                ColoredOutput.success(f"Arquivo criado: {filename}")
            
            # Torna main.py executável
            main_py = self.app_dir / "main.py"
            main_py.chmod(main_py.stat().st_mode | 0o111)
            
            return True
            
        except Exception as e:
            ColoredOutput.error(f"Erro ao criar arquivos: {e}")
            return False
    
    def generate(self) -> bool:
        """Gera o app completo"""
        ColoredOutput.header(f"Gerando App: {self.app_title}")
        
        # Cria diretório
        if not self.create_directory_structure():
            return False
        
        # Cria arquivos
        if not self.create_files():
            return False
        
        # Resumo final
        ColoredOutput.section(
            "✅ App Criado com Sucesso!",
            f"""
Localização: {self.app_dir}
Tipo: {self.app_type}
Arquivos criados: 4

Próximos passos:
1. cd apps/{self.app_name}
2. pip install -r requirements.txt
3. python main.py --help
4. Customize conforme necessário!
            """
        )
        
        return True


def main():
    """Função principal do gerador"""
    parser = argparse.ArgumentParser(
        description="🛠️ Gerador de Apps RAG - Cria estrutura básica para novos apps",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python create_app.py my-chat-app --type chat
  python create_app.py data-analyzer --type analysis --author "João Silva"
  python create_app.py api-gateway --type api

Tipos disponíveis:
  basic    - App básico com template simples
  chat     - App de chat interativo
  analysis - App de análise de dados
  api      - API REST com endpoints RAG
        """
    )
    
    parser.add_argument(
        "app_name",
        help="Nome do app (será convertido para kebab-case)"
    )
    
    parser.add_argument(
        "--type",
        choices=["basic", "chat", "analysis", "api"],
        default="basic",
        help="Tipo de app a criar (default: basic)"
    )
    
    parser.add_argument(
        "--author",
        default="RAG Team",
        help="Nome do autor (default: RAG Team)"
    )
    
    parser.add_argument(
        "--force",
        action="store_true",
        help="Sobrescrever se o app já existir"
    )
    
    args = parser.parse_args()
    
    # Se --force, remove diretório existente
    if args.force:
        app_dir = Path(__file__).parent.parent / "apps" / args.app_name.lower().replace(" ", "-")
        if app_dir.exists():
            import shutil
            shutil.rmtree(app_dir)
            ColoredOutput.warning(f"Diretório existente removido: {app_dir}")
    
    # Cria o gerador e executa
    generator = AppGenerator(
        app_name=args.app_name,
        app_type=args.type,
        author=args.author
    )
    
    success = generator.generate()
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())