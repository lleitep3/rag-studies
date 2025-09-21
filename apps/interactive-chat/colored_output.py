#!/usr/bin/env python3
"""
🎨 Colored Output Utility
========================

Utilitário para exibir texto colorido e formatado no terminal.
Fornece métodos convenientes para diferentes tipos de mensagens.
"""


class ColoredOutput:
    """Classe para output colorido no terminal"""
    
    # Cores ANSI
    RESET = '\033[0m'
    BOLD = '\033[1m'
    
    # Cores de texto
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
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
    def print_colored(cls, text: str, color: str = '', bg: str = '', bold: bool = False):
        """Imprime texto colorido"""
        style = ''
        if bold:
            style += cls.BOLD
        if color:
            style += color
        if bg:
            style += bg
            
        print(f"{style}{text}{cls.RESET}")
    
    @classmethod
    def header(cls, text: str):
        """Cabeçalho em destaque"""
        cls.print_colored(f"\n🤖 {text}", cls.CYAN, bold=True)
        cls.print_colored("=" * (len(text) + 3), cls.CYAN)
    
    @classmethod
    def success(cls, text: str):
        """Mensagem de sucesso"""
        cls.print_colored(f"✅ {text}", cls.GREEN)
    
    @classmethod
    def warning(cls, text: str):
        """Mensagem de aviso"""
        cls.print_colored(f"⚠️ {text}", cls.YELLOW)
    
    @classmethod
    def error(cls, text: str):
        """Mensagem de erro"""
        cls.print_colored(f"❌ {text}", cls.RED)
    
    @classmethod
    def info(cls, text: str):
        """Informação"""
        cls.print_colored(f"ℹ️ {text}", cls.BLUE)
    
    @classmethod
    def question(cls, text: str):
        """Pergunta do usuário"""
        cls.print_colored(f"❓ {text}", cls.MAGENTA, bold=True)
    
    @classmethod
    def answer(cls, text: str):
        """Resposta do assistente"""
        cls.print_colored(f"💡 {text}", cls.GREEN)


def demo():
    """Demonstra todas as cores disponíveis"""
    print("\n🎨 Demonstração de Cores:")
    print("=" * 30)
    
    ColoredOutput.header("Cabeçalho de Exemplo")
    ColoredOutput.success("Esta é uma mensagem de sucesso")
    ColoredOutput.warning("Esta é uma mensagem de aviso")
    ColoredOutput.error("Esta é uma mensagem de erro")
    ColoredOutput.info("Esta é uma mensagem informativa")
    ColoredOutput.question("Esta é uma pergunta?")
    ColoredOutput.answer("Esta é uma resposta")
    
    print("\nCores básicas:")
    colors = [
        (ColoredOutput.RED, "Texto vermelho"),
        (ColoredOutput.GREEN, "Texto verde"),
        (ColoredOutput.BLUE, "Texto azul"),
        (ColoredOutput.YELLOW, "Texto amarelo"),
        (ColoredOutput.MAGENTA, "Texto magenta"),
        (ColoredOutput.CYAN, "Texto ciano"),
    ]
    
    for color, text in colors:
        ColoredOutput.print_colored(text, color)
    
    print("\nTexto em negrito:")
    ColoredOutput.print_colored("Texto em negrito", ColoredOutput.WHITE, bold=True)


if __name__ == "__main__":
    demo()