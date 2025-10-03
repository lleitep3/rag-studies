"""
🎨 Colored Output Utility
========================

Utilitário para exibir texto colorido e formatado no terminal.
Fornece métodos convenientes para diferentes tipos de mensagens.
"""

from typing import Optional


class ColoredOutput:
    """Classe para output colorido no terminal"""
    
    # Cores ANSI
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    
    # Cores de texto
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Cores bright (mais claras)
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    
    # Cores de fundo
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'
    
    @classmethod
    def print_colored(
        cls, 
        text: str, 
        color: str = '', 
        bg: str = '', 
        bold: bool = False,
        dim: bool = False,
        italic: bool = False,
        underline: bool = False
    ) -> None:
        """
        Imprime texto colorido com várias opções de estilo.
        
        Args:
            text: Texto a ser impresso
            color: Cor do texto (usar constantes da classe)
            bg: Cor de fundo (usar constantes BG_*)
            bold: Texto em negrito
            dim: Texto esmaecido
            italic: Texto em itálico
            underline: Texto sublinhado
        """
        style = ''
        if bold:
            style += cls.BOLD
        if dim:
            style += cls.DIM
        if italic:
            style += cls.ITALIC
        if underline:
            style += cls.UNDERLINE
        if color:
            style += color
        if bg:
            style += bg
            
        print(f"{style}{text}{cls.RESET}")
    
    @classmethod
    def header(cls, text: str, emoji: str = "🤖") -> None:
        """Cabeçalho em destaque"""
        cls.print_colored(f"\n{emoji} {text}", cls.CYAN, bold=True)
        cls.print_colored("=" * (len(text) + len(emoji) + 2), cls.CYAN)
    
    @classmethod
    def success(cls, text: str, prefix: str = "✅") -> None:
        """Mensagem de sucesso"""
        cls.print_colored(f"{prefix} {text}", cls.GREEN)
    
    @classmethod
    def warning(cls, text: str, prefix: str = "⚠️") -> None:
        """Mensagem de aviso"""
        cls.print_colored(f"{prefix} {text}", cls.YELLOW)
    
    @classmethod
    def error(cls, text: str, prefix: str = "❌") -> None:
        """Mensagem de erro"""
        cls.print_colored(f"{prefix} {text}", cls.RED, bold=True)
    
    @classmethod
    def info(cls, text: str, prefix: str = "ℹ️") -> None:
        """Informação"""
        cls.print_colored(f"{prefix} {text}", cls.BLUE)
    
    @classmethod
    def question(cls, text: str, prefix: str = "❓") -> None:
        """Pergunta do usuário"""
        cls.print_colored(f"{prefix} {text}", cls.MAGENTA, bold=True)
    
    @classmethod
    def answer(cls, text: str, prefix: str = "💡") -> None:
        """Resposta do assistente"""
        cls.print_colored(f"{prefix} {text}", cls.GREEN)
    
    @classmethod
    def section(cls, title: str, content: str, color: Optional[str] = None) -> None:
        """Exibe uma seção formatada com título e conteúdo"""
        color = color or cls.CYAN
        cls.print_colored(f"\n▶ {title}", color, bold=True)
        cls.print_colored("-" * (len(title) + 2), color)
        print(content)
    
    @classmethod
    def progress(cls, current: int, total: int, label: str = "Progress") -> None:
        """Exibe uma barra de progresso simples"""
        percentage = int((current / total) * 100)
        bar_length = 30
        filled_length = int(bar_length * current // total)
        bar = '█' * filled_length + '░' * (bar_length - filled_length)
        
        color = cls.GREEN if percentage >= 80 else cls.YELLOW if percentage >= 50 else cls.RED
        cls.print_colored(
            f"{label}: [{bar}] {percentage}% ({current}/{total})", 
            color
        )
    
    @classmethod
    def table_row(cls, *columns, widths: Optional[list] = None, colors: Optional[list] = None) -> None:
        """
        Imprime uma linha de tabela formatada.
        
        Args:
            columns: Valores das colunas
            widths: Larguras das colunas (opcional)
            colors: Cores das colunas (opcional)
        """
        if widths is None:
            widths = [20] * len(columns)
        if colors is None:
            colors = [cls.WHITE] * len(columns)
            
        row = ""
        for col, width, color in zip(columns, widths, colors):
            formatted_col = str(col)[:width].ljust(width)
            row += f"{color}{formatted_col}{cls.RESET} "
        
        print(row)


def demo():
    """Demonstra todas as funcionalidades disponíveis"""
    print("\n🎨 Demonstração de ColoredOutput")
    print("=" * 40)
    
    # Mensagens básicas
    ColoredOutput.header("Tipos de Mensagens")
    ColoredOutput.success("Operação realizada com sucesso!")
    ColoredOutput.warning("Atenção: Este é um aviso importante")
    ColoredOutput.error("Erro: Algo deu errado")
    ColoredOutput.info("Informação útil sobre o processo")
    ColoredOutput.question("Qual é a sua pergunta?")
    ColoredOutput.answer("Esta é a resposta")
    
    # Seção formatada
    ColoredOutput.section(
        "Exemplo de Seção",
        "Este é o conteúdo da seção.\nPode ter múltiplas linhas.\nMuito útil para organizar output."
    )
    
    # Barra de progresso
    print("\n📊 Demonstração de Progresso:")
    for i in range(0, 11, 2):
        ColoredOutput.progress(i, 10, "Download")
    
    # Tabela
    print("\n📋 Demonstração de Tabela:")
    ColoredOutput.table_row("Nome", "Idade", "Cidade", widths=[15, 10, 15])
    ColoredOutput.table_row("-"*15, "-"*10, "-"*15, widths=[15, 10, 15])
    ColoredOutput.table_row(
        "João Silva", "28", "São Paulo",
        widths=[15, 10, 15],
        colors=[ColoredOutput.CYAN, ColoredOutput.YELLOW, ColoredOutput.GREEN]
    )
    ColoredOutput.table_row(
        "Maria Santos", "32", "Rio de Janeiro",
        widths=[15, 10, 15],
        colors=[ColoredOutput.CYAN, ColoredOutput.YELLOW, ColoredOutput.GREEN]
    )
    
    # Estilos de texto
    print("\n🎯 Demonstração de Estilos:")
    ColoredOutput.print_colored("Texto em negrito", ColoredOutput.WHITE, bold=True)
    ColoredOutput.print_colored("Texto em itálico", ColoredOutput.WHITE, italic=True)
    ColoredOutput.print_colored("Texto sublinhado", ColoredOutput.WHITE, underline=True)
    ColoredOutput.print_colored("Texto esmaecido", ColoredOutput.WHITE, dim=True)
    ColoredOutput.print_colored(
        "Texto com múltiplos estilos", 
        ColoredOutput.BRIGHT_CYAN, 
        bold=True, 
        underline=True
    )
    
    # Cores disponíveis
    print("\n🌈 Todas as Cores Disponíveis:")
    colors = [
        ("Normal", [
            (ColoredOutput.RED, "Vermelho"),
            (ColoredOutput.GREEN, "Verde"),
            (ColoredOutput.BLUE, "Azul"),
            (ColoredOutput.YELLOW, "Amarelo"),
            (ColoredOutput.MAGENTA, "Magenta"),
            (ColoredOutput.CYAN, "Ciano"),
        ]),
        ("Bright", [
            (ColoredOutput.BRIGHT_RED, "Vermelho Claro"),
            (ColoredOutput.BRIGHT_GREEN, "Verde Claro"),
            (ColoredOutput.BRIGHT_BLUE, "Azul Claro"),
            (ColoredOutput.BRIGHT_YELLOW, "Amarelo Claro"),
            (ColoredOutput.BRIGHT_MAGENTA, "Magenta Claro"),
            (ColoredOutput.BRIGHT_CYAN, "Ciano Claro"),
        ])
    ]
    
    for category, color_list in colors:
        print(f"\n{category}:")
        for color, text in color_list:
            ColoredOutput.print_colored(f"  {text}", color)


if __name__ == "__main__":
    demo()