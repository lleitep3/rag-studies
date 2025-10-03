#!/usr/bin/env python3
"""
📋 List Apps - Listador de Aplicações RAG
==========================================

Lista todas as aplicações disponíveis na pasta apps/ com informações detalhadas.
"""

import sys
import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

# Adiciona src ao path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.helpers.colored_output import ColoredOutput


def get_app_info(app_dir: Path) -> Optional[Dict]:
    """
    Extrai informações de um app.
    
    Args:
        app_dir: Diretório do app
        
    Returns:
        Dicionário com informações do app ou None se não for válido
    """
    if not app_dir.is_dir():
        return None
    
    info = {
        "name": app_dir.name,
        "path": str(app_dir),
        "has_main": (app_dir / "main.py").exists(),
        "has_readme": (app_dir / "README.md").exists(),
        "has_config": (app_dir / "config.json").exists() or (app_dir / "config.example.json").exists(),
        "has_requirements": (app_dir / "requirements.txt").exists(),
        "type": "unknown",
        "created": None,
        "modified": None,
        "size": 0
    }
    
    # Tenta obter tipo do config
    config_file = app_dir / "config.example.json"
    if not config_file.exists():
        config_file = app_dir / "config.json"
    
    if config_file.exists():
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
                info["type"] = config.get("app_type", "unknown")
        except:
            pass
    
    # Obtém datas
    if (app_dir / "main.py").exists():
        main_stat = (app_dir / "main.py").stat()
        info["created"] = datetime.fromtimestamp(main_stat.st_ctime).strftime("%Y-%m-%d %H:%M")
        info["modified"] = datetime.fromtimestamp(main_stat.st_mtime).strftime("%Y-%m-%d %H:%M")
    
    # Calcula tamanho total
    for file in app_dir.rglob("*"):
        if file.is_file():
            info["size"] += file.stat().st_size
    
    # Formata tamanho
    size_kb = info["size"] / 1024
    if size_kb < 1024:
        info["size_str"] = f"{size_kb:.1f} KB"
    else:
        info["size_str"] = f"{size_kb/1024:.1f} MB"
    
    return info


def get_app_status_icon(info: Dict) -> str:
    """Retorna ícone de status baseado na completude do app"""
    if not info["has_main"]:
        return "❌"
    elif info["has_main"] and info["has_readme"] and info["has_config"] and info["has_requirements"]:
        return "✅"
    elif info["has_main"] and info["has_readme"]:
        return "🔄"
    else:
        return "⚠️"


def get_type_emoji(app_type: str) -> str:
    """Retorna emoji baseado no tipo do app"""
    emojis = {
        "chat": "💬",
        "analysis": "📊",
        "api": "🌐",
        "basic": "🎯",
        "unknown": "❓"
    }
    return emojis.get(app_type, "📦")


def list_apps(detailed: bool = False, filter_type: Optional[str] = None):
    """
    Lista todos os apps disponíveis.
    
    Args:
        detailed: Se True, mostra informações detalhadas
        filter_type: Filtra por tipo de app
    """
    apps_dir = project_root / "apps"
    
    if not apps_dir.exists():
        ColoredOutput.warning("Pasta 'apps' não encontrada.")
        ColoredOutput.info("Use 'python scripts/create_app.py' para criar seu primeiro app!")
        return
    
    # Coleta informações dos apps
    apps_info = []
    for app_dir in sorted(apps_dir.iterdir()):
        if app_dir.is_dir() and not app_dir.name.startswith("__"):
            info = get_app_info(app_dir)
            if info:
                if filter_type and info["type"] != filter_type:
                    continue
                apps_info.append(info)
    
    if not apps_info:
        if filter_type:
            ColoredOutput.warning(f"Nenhum app do tipo '{filter_type}' encontrado.")
        else:
            ColoredOutput.warning("Nenhum app encontrado.")
        ColoredOutput.info("Use 'python scripts/create_app.py' para criar um novo app!")
        return
    
    # Exibe cabeçalho
    ColoredOutput.header(f"📱 Apps RAG Disponíveis ({len(apps_info)} apps)")
    
    if detailed:
        # Modo detalhado - uma seção por app
        for info in apps_info:
            status = get_app_status_icon(info)
            emoji = get_type_emoji(info["type"])
            
            ColoredOutput.section(
                f"{status} {emoji} {info['name']}",
                f"""Tipo: {info['type']}
Caminho: {info['path']}
Criado: {info['created'] or 'N/A'}
Modificado: {info['modified'] or 'N/A'}
Tamanho: {info['size_str']}

Arquivos:
  main.py:          {'✅' if info['has_main'] else '❌'}
  README.md:        {'✅' if info['has_readme'] else '❌'}
  config:           {'✅' if info['has_config'] else '❌'}
  requirements.txt: {'✅' if info['has_requirements'] else '❌'}"""
            )
    else:
        # Modo tabela
        print()
        # Cabeçalho da tabela
        ColoredOutput.table_row(
            "Status", "App", "Tipo", "Tamanho", "Modificado",
            widths=[8, 20, 10, 10, 20]
        )
        ColoredOutput.table_row(
            "-"*8, "-"*20, "-"*10, "-"*10, "-"*20,
            widths=[8, 20, 10, 10, 20]
        )
        
        # Linhas da tabela
        for info in apps_info:
            status = get_app_status_icon(info)
            emoji = get_type_emoji(info["type"])
            
            ColoredOutput.table_row(
                f"{status} {emoji}",
                info["name"],
                info["type"],
                info["size_str"],
                info["modified"] or "N/A",
                widths=[8, 20, 10, 10, 20]
            )
        
        print()
        
        # Legenda
        ColoredOutput.info(
            "Legenda: ✅ Completo | 🔄 Em progresso | ⚠️ Incompleto | ❌ Inválido"
        )
    
    # Estatísticas
    print()
    ColoredOutput.section(
        "📊 Estatísticas",
        f"""Total de Apps: {len(apps_info)}
Por Tipo:
  💬 Chat:     {sum(1 for a in apps_info if a['type'] == 'chat')}
  📊 Analysis: {sum(1 for a in apps_info if a['type'] == 'analysis')}
  🌐 API:      {sum(1 for a in apps_info if a['type'] == 'api')}
  🎯 Basic:    {sum(1 for a in apps_info if a['type'] == 'basic')}
  ❓ Unknown:  {sum(1 for a in apps_info if a['type'] == 'unknown')}

Tamanho Total: {sum(a['size'] for a in apps_info) / 1024:.1f} KB"""
    )


def main():
    """Função principal"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="📋 Lista todas as aplicações RAG disponíveis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python scripts/list_apps.py              # Lista simples
  python scripts/list_apps.py --detailed   # Lista detalhada
  python scripts/list_apps.py --type chat  # Apenas apps de chat
        """
    )
    
    parser.add_argument(
        "-d", "--detailed",
        action="store_true",
        help="Mostrar informações detalhadas de cada app"
    )
    
    parser.add_argument(
        "-t", "--type",
        choices=["basic", "chat", "analysis", "api"],
        help="Filtrar por tipo de app"
    )
    
    args = parser.parse_args()
    
    list_apps(detailed=args.detailed, filter_type=args.type)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())