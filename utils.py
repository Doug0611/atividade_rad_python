from datetime import datetime
import os
from random import sample


class Tools:

    def _generate_enrollment(self) -> str:
        numbers = list(range(10))
        date = datetime.now().strftime("%Y%m%d")
        shuffle = sample(numbers, k=4)
        return ''.join([date] + [str(char) for char in shuffle])

    def data(self, name: str, gender: str, av: tuple[float], absences: int) -> str:
        registration = self._generate_enrollment()
        avarage = self.mean(av)
        return f"""
       {registration};{name};{gender};{list(av)};{avarage};{absences}
        """

    def mean(self, test_scores: list[float]) -> float:
        return round(sum(test_scores) / len(test_scores), 1)

    def clear_terminal(self) -> None:
        os.system("cls")

    def menu(self) -> None:
        print("\033[1;36m MENU \033[0;0m".center(50, "="))
        print("""
    1 - Cadastrar aluno
    2 - Remover aluno
    3 - Buscar aluno 
    4 - Relatórios
    5 - Configurações 
    6 - Sair
        """)

    def menu_reports(self) -> None:
        print("\033[1;36m RELATÓRIOS \033[0;0m".center(50, "="))
        print("""
    1 - Listar todos os alunos
    2 - Listar alunos aprovados
    3 - Listar alunos reprovados por faltas
    4 - Listar dados completos do aluno de maior média
    5 - Listar dados completos do aluno de menor média 
        """)
