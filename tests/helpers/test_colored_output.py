"""
Testes para ColoredOutput Helper
=================================

Testa a funcionalidade de output colorido no terminal.
"""

import pytest
from unittest.mock import patch, call
import sys
from pathlib import Path

# Adiciona src ao path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.helpers.colored_output import ColoredOutput


class TestColoredOutput:
    """Testes para a classe ColoredOutput"""
    
    @pytest.mark.unit
    def test_color_constants(self):
        """Testa se as constantes de cor estão definidas corretamente"""
        assert ColoredOutput.RESET == '\033[0m'
        assert ColoredOutput.BOLD == '\033[1m'
        assert ColoredOutput.RED == '\033[31m'
        assert ColoredOutput.GREEN == '\033[32m'
        assert ColoredOutput.BLUE == '\033[34m'
        assert ColoredOutput.CYAN == '\033[36m'
        assert ColoredOutput.BRIGHT_CYAN == '\033[96m'
    
    @pytest.mark.unit
    @patch('builtins.print')
    def test_print_colored_basic(self, mock_print):
        """Testa impressão básica colorida"""
        ColoredOutput.print_colored("Test", ColoredOutput.RED)
        
        mock_print.assert_called_once_with('\033[31mTest\033[0m')
    
    @pytest.mark.unit
    @patch('builtins.print')
    def test_print_colored_with_styles(self, mock_print):
        """Testa impressão com múltiplos estilos"""
        ColoredOutput.print_colored(
            "Test", 
            ColoredOutput.BLUE, 
            bold=True, 
            underline=True
        )
        
        expected = '\033[1m\033[4m\033[34mTest\033[0m'
        mock_print.assert_called_once_with(expected)
    
    @pytest.mark.unit
    @patch('builtins.print')
    def test_print_colored_with_background(self, mock_print):
        """Testa impressão com cor de fundo"""
        ColoredOutput.print_colored(
            "Test",
            ColoredOutput.WHITE,
            bg=ColoredOutput.BG_BLUE
        )
        
        expected = '\033[37m\033[44mTest\033[0m'
        mock_print.assert_called_once_with(expected)
    
    @pytest.mark.unit
    @patch('builtins.print')
    def test_header(self, mock_print):
        """Testa método header"""
        ColoredOutput.header("Test Header")
        
        calls = mock_print.call_args_list
        assert len(calls) == 2
        # Verifica que o header contém o emoji e o texto
        assert "Test Header" in calls[0][0][0]
        assert "🤖" in calls[0][0][0]
        # Verifica que a linha de separação tem o comprimento correto
        assert "=" in calls[1][0][0]
    
    @pytest.mark.unit
    @patch('builtins.print')
    def test_header_custom_emoji(self, mock_print):
        """Testa header com emoji customizado"""
        ColoredOutput.header("Test", emoji="🎯")
        
        first_call = mock_print.call_args_list[0][0][0]
        assert "🎯" in first_call
        assert "Test" in first_call
    
    @pytest.mark.unit
    @patch('builtins.print')
    def test_success_message(self, mock_print):
        """Testa mensagem de sucesso"""
        ColoredOutput.success("Operation successful")
        
        call_args = mock_print.call_args[0][0]
        assert "✅" in call_args
        assert "Operation successful" in call_args
        assert ColoredOutput.GREEN in call_args
    
    @pytest.mark.unit
    @patch('builtins.print')
    def test_warning_message(self, mock_print):
        """Testa mensagem de aviso"""
        ColoredOutput.warning("Be careful")
        
        call_args = mock_print.call_args[0][0]
        assert "⚠️" in call_args
        assert "Be careful" in call_args
        assert ColoredOutput.YELLOW in call_args
    
    @pytest.mark.unit
    @patch('builtins.print')
    def test_error_message(self, mock_print):
        """Testa mensagem de erro"""
        ColoredOutput.error("Something went wrong")
        
        call_args = mock_print.call_args[0][0]
        assert "❌" in call_args
        assert "Something went wrong" in call_args
        assert ColoredOutput.RED in call_args
        assert ColoredOutput.BOLD in call_args
    
    @pytest.mark.unit
    @patch('builtins.print')
    def test_info_message(self, mock_print):
        """Testa mensagem informativa"""
        ColoredOutput.info("Important information")
        
        call_args = mock_print.call_args[0][0]
        assert "ℹ️" in call_args
        assert "Important information" in call_args
        assert ColoredOutput.BLUE in call_args
    
    @pytest.mark.unit
    @patch('builtins.print')
    def test_question_message(self, mock_print):
        """Testa mensagem de pergunta"""
        ColoredOutput.question("What is your name?")
        
        call_args = mock_print.call_args[0][0]
        assert "❓" in call_args
        assert "What is your name?" in call_args
        assert ColoredOutput.MAGENTA in call_args
    
    @pytest.mark.unit
    @patch('builtins.print')
    def test_answer_message(self, mock_print):
        """Testa mensagem de resposta"""
        ColoredOutput.answer("The answer is 42")
        
        call_args = mock_print.call_args[0][0]
        assert "💡" in call_args
        assert "The answer is 42" in call_args
        assert ColoredOutput.GREEN in call_args
    
    @pytest.mark.unit
    @patch('builtins.print')
    def test_custom_prefix(self, mock_print):
        """Testa mensagens com prefixo customizado"""
        ColoredOutput.success("Test", prefix="🚀")
        
        call_args = mock_print.call_args[0][0]
        assert "🚀" in call_args
        assert "✅" not in call_args
    
    @pytest.mark.unit
    @patch('builtins.print')
    def test_section(self, mock_print):
        """Testa exibição de seção"""
        ColoredOutput.section("Title", "Content\nMultiline")
        
        calls = mock_print.call_args_list
        assert len(calls) == 3  # Título, separador, conteúdo
        
        # Verifica título
        assert "▶ Title" in calls[0][0][0]
        # Verifica separador
        assert "-" in calls[1][0][0]
        # Verifica conteúdo
        assert "Content\nMultiline" == calls[2][0][0]
    
    @pytest.mark.unit
    @patch('builtins.print')
    def test_progress_bar(self, mock_print):
        """Testa barra de progresso"""
        # Teste 0%
        ColoredOutput.progress(0, 10, "Test")
        call_args = mock_print.call_args[0][0]
        assert "0%" in call_args
        assert "░" in call_args  # Barra vazia
        assert ColoredOutput.RED in call_args
        
        mock_print.reset_mock()
        
        # Teste 50%
        ColoredOutput.progress(5, 10, "Test")
        call_args = mock_print.call_args[0][0]
        assert "50%" in call_args
        assert "█" in call_args  # Barra parcialmente cheia
        assert ColoredOutput.YELLOW in call_args
        
        mock_print.reset_mock()
        
        # Teste 100%
        ColoredOutput.progress(10, 10, "Test")
        call_args = mock_print.call_args[0][0]
        assert "100%" in call_args
        assert ColoredOutput.GREEN in call_args
    
    @pytest.mark.unit
    @patch('builtins.print')
    def test_table_row_default(self, mock_print):
        """Testa linha de tabela com valores padrão"""
        ColoredOutput.table_row("Col1", "Col2", "Col3")
        
        call_args = mock_print.call_args[0][0]
        assert "Col1" in call_args
        assert "Col2" in call_args
        assert "Col3" in call_args
        # Verifica espaçamento padrão
        assert len(call_args) > 60  # 3 colunas x 20 chars cada
    
    @pytest.mark.unit
    @patch('builtins.print')
    def test_table_row_custom_widths(self, mock_print):
        """Testa linha de tabela com larguras customizadas"""
        ColoredOutput.table_row(
            "Short", "Medium Column", "Long Column Text",
            widths=[5, 10, 15]
        )
        
        call_args = mock_print.call_args[0][0]
        # Verifica truncamento
        assert "Short" in call_args
        assert "Medium Col" in call_args  # Truncado para 10 chars
    
    @pytest.mark.unit
    @patch('builtins.print')
    def test_table_row_custom_colors(self, mock_print):
        """Testa linha de tabela com cores customizadas"""
        ColoredOutput.table_row(
            "Red", "Green", "Blue",
            colors=[ColoredOutput.RED, ColoredOutput.GREEN, ColoredOutput.BLUE]
        )
        
        call_args = mock_print.call_args[0][0]
        assert ColoredOutput.RED in call_args
        assert ColoredOutput.GREEN in call_args
        assert ColoredOutput.BLUE in call_args
    
    @pytest.mark.unit
    @patch('builtins.print')
    def test_all_style_combinations(self, mock_print):
        """Testa todas as combinações de estilo"""
        styles = {
            'bold': True,
            'dim': True,
            'italic': True,
            'underline': True
        }
        
        ColoredOutput.print_colored("Test", ColoredOutput.WHITE, **styles)
        
        call_args = mock_print.call_args[0][0]
        assert ColoredOutput.BOLD in call_args
        assert ColoredOutput.DIM in call_args
        assert ColoredOutput.ITALIC in call_args
        assert ColoredOutput.UNDERLINE in call_args


class TestColoredOutputDemo:
    """Testa a função demo"""
    
    @pytest.mark.unit
    @patch('builtins.print')
    def test_demo_runs_without_error(self, mock_print):
        """Testa se a demo executa sem erros"""
        from src.helpers.colored_output import demo
        
        # Não deve lançar exceções
        demo()
        
        # Verifica que várias chamadas foram feitas
        assert mock_print.call_count > 20