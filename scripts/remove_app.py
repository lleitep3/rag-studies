#!/usr/bin/env python3
"""
🗑️ Remove App - Removedor de Aplicações RAG
============================================

Remove aplicações RAG com confirmação de segurança.
"""

import sys
import shutil
from pathlib import Path
from typing import Optional

# Adiciona src ao path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.helpers.colored_output import ColoredOutput


def confirm_removal(app_name: str, app_path: Path) -> bool:
    """
    Solicita confirmação do usuário para remover o app.
    
    Args:
        app_name: Nome do app
        app_path: Caminho do app
        
    Returns:
        True se confirmado, False caso contrário
    """
    ColoredOutput.warning(f"⚠️  ATENÇÃO: Esta ação irá remover permanentemente o app '{app_name}'")
    ColoredOutput.info(f"Caminho: {app_path}")
    
    # Lista arquivos que serão removidos
    files = list(app_path.rglob("*"))
    if files:
        ColoredOutput.section(
            "Arquivos a serem removidos:",
            "\n".join(f"  • {f.relative_to(app_path)}" for f in files[:10])
        )
        if len(files) > 10:
            ColoredOutput.info(f"  ... e mais {len(files) - 10} arquivos")
    
    # Solicita confirmação
    print()
    response = input("🤔 Tem certeza que deseja remover este app? [s/N]: ").strip().lower()
    
    return response in ['s', 'sim', 'y', 'yes']


def remove_app(app_name: str, force: bool = False) -> bool:
    """
    Remove um app do projeto.
    
    Args:
        app_name: Nome do app a remover
        force: Se True, remove sem confirmação
        
    Returns:
        True se removido com sucesso, False caso contrário
    """
    apps_dir = project_root / "apps"
    app_path = apps_dir / app_name
    
    # Verifica se o app existe
    if not app_path.exists():
        ColoredOutput.error(f"❌ App '{app_name}' não encontrado")
        ColoredOutput.info("Use 'python scripts/list_apps.py' para ver apps disponíveis")
        return False
    
    if not app_path.is_dir():
        ColoredOutput.error(f"❌ '{app_name}' não é um diretório de app válido")
        return False
    
    # Solicita confirmação se não for forçado
    if not force:
        if not confirm_removal(app_name, app_path):
            ColoredOutput.info("👍 Operação cancelada")
            return False
    
    # Remove o app
    try:
        shutil.rmtree(app_path)
        ColoredOutput.success(f"✅ App '{app_name}' removido com sucesso!")
        
        # Mostra estatísticas
        remaining_apps = len([d for d in apps_dir.iterdir() if d.is_dir() and not d.name.startswith("__")])
        ColoredOutput.info(f"📊 Apps restantes: {remaining_apps}")
        
        return True
        
    except PermissionError:
        ColoredOutput.error(f"❌ Erro de permissão ao remover '{app_name}'")
        ColoredOutput.info("Verifique as permissões do diretório")
        return False
    except Exception as e:
        ColoredOutput.error(f"❌ Erro ao remover app: {e}")
        return False


def main():
    """Função principal"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="🗑️ Remove aplicações RAG com segurança",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python scripts/remove_app.py meu-app          # Remove com confirmação
  python scripts/remove_app.py meu-app --force  # Remove sem confirmação
  
ATENÇÃO: Esta operação é IRREVERSÍVEL!
        """
    )
    
    parser.add_argument(
        "app_name",
        help="Nome do app a remover"
    )
    
    parser.add_argument(
        "-f", "--force",
        action="store_true",
        help="Remover sem confirmação (USE COM CUIDADO!)"
    )
    
    args = parser.parse_args()
    
    # Header
    ColoredOutput.header("🗑️ Removedor de Apps RAG")
    
    # Remove o app
    success = remove_app(args.app_name, force=args.force)
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())