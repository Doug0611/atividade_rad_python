r"""
1.Crie um programa em python que realize o registro acadêmico de uma turma. Para tal, o seguinte 
menu deve ser exibido e suas funcionalidades implementadas para que os dados sejam persistidos e 
mantidos e arquivo texto.

Os dados a serem cadastrados dos alunos são:

- Matrícula
- Nome 
- Nota 1 
- Nota 2 
- Nota 3 
- Sexo 
- Quantidade de faltas 
* média

Itens de configuração a serem cadastrados:
- Nome do professor
- Nome da disciplina
- Carga horária da disciplina
- Ano da disciplina


===========================================
                MENU
===========================================

1 - Cadastrar Aluno
2 - Remover Aluno
3 - Buscar Aluno por matrícula (listando todos os dados desse aluno, inclusive a média)
4 - Relatórios:
     4.1 - Listar todos os alunos
     4.2 - Listar alunos aprovados (Critério de aprovação média >= 6,0 e frequência >= 75%)
     4.3 - Listar alunos reprovados por faltas (frequência < 75%)
     4.4 - Listar dados completos do aluno de maior média
     4.5 - Listar dados completos do aluno de menor média
 5 - Configurações (nome disciplina, professor, carga horaria, ano da disciplina).
 6 - Sair  

Obs: Todos os relatorios devem conter em tela o nome do professor e disciplina, ano da disciplina   
"""
import sys
from time import sleep
from file import File, Report
from utils import Tools
from validator import Validator


tools = Tools()
report = Report()
student = File("alunos.txt")
settings = File("materia.txt")


def operation(option: int) -> str:
    match option:
        case 1:
            tools.clear_terminal()
            print("\033[1;36m CADASTRO DE ALUNO \033[0;0m".center(60, "="))
            try:
                print()
                name: str = str(input("Nome completo >> ")).upper().strip()
                if not Validator.validate_field_name(name):
                    print("""
                    \n\033[1;91m>> PREENCHIMENTO DO CAMPO NOME INVÁLIDO\033[0;0m
                    """.strip("\t"))
                    sleep(1.5)
                    return
                gender: str = str(input("Sexo (M / F) >> ")).upper().strip()
                if not Validator.validate_field_gender(gender):
                    print("""
                    \n\033[1;91m>> PREENCHIMENTO DO CAMPO SEXO INVÁLIDO\033[0;0m
                    """.strip("\t"))
                    sleep(1.5)
                    return
                av1: float = float(input("Primeira nota >> "))
                av2: float = float(input("Segunda nota >> "))
                av3: float = float(input("Terceira nota >> "))
                if not Validator.validade_field_scores(av1, av2, av3):
                    print("""
                    \n\033[1;91m>> PREENCHIMENTO DO CAMPO NOTA INVÁLIDO\033[0;0m
                    """.strip("\t"))
                    sleep(1.5)
                    return
                absences: int = int(input("N° de faltas >> "))
            except ValueError:
                print("\n\033[1;91m>> DADO INVÁLIDO\033[0;0m")
                sleep(1)
            else:
                insert = student.insert_student(
                    name=name,
                    gender=gender,
                    av=(av1, av2, av3),
                    absences=absences,
                    func=tools.data
                )
                print(insert)
                sleep(1.5)

        case 2:
            tools.clear_terminal()
            print("\033[1;36m REMOVER ALUNO \033[0;0m".center(60, "="))
            try:
                print()
                count: int = 0
                for line in report.all_lines():
                    print(line)
                    count += 1
                print("%d REGISTRO(S) LISTADOS." % count)
                if student.check():
                    indice: int = int(input("\nINFORME O ÍNDICE >>> "))
                    remove: str = student.delete(indice)
                    print(remove)
                    sleep(1.1)
                else:
                    print(
                        "\n\033[1;93m>> NÃO TEM REGISTROS PARA REMOVER\033[0;0m")
                    sleep(1.5)
            except ValueError:
                print("\n\033[1;91m>> DADO INVÁLIDO\033[0;0m")
                sleep(1.5)

        case 3:
            tools.clear_terminal()
            print("\033[1;36m BUSCAR ALUNO \033[0;0m".center(60, "="))
            try:
                print()
                if student.check():
                    cod: int = int(input("\nN° DA MATRÍCULA >>> "))
                    search: str = student.search(cod)
                    print()
                    print(search)
                    sleep(5)
                else:
                    print(
                        "\n\033[1;93m>> SEM REGISTROS PARA CONSULTAR\033[0;0m")
                    sleep(1.5)
            except ValueError:
                print("\n\033[1;91m>> DADO INVÁLIDO\033[0;0m")
                sleep(1)

        case 4:
            tools.clear_terminal()
            tools.menu_reports()
            try:
                options = int(input(">> "))
                match options:
                    case 1:
                        while True:
                            tools.clear_terminal()
                            print(
                                "\033[1;36m TODOS OS ALUNOS \033[0;0m".center(60, "="))
                            print()
                            count = 0
                            for line in report.all_lines():
                                print(line)
                                count += 1
                            print("\n%d REGISTRO(S) LISTADOS." % count)
                            close = str(
                                input("\n<< PRESSIONE 0 PARA SAIR >> "))
                            if close.isdigit():
                                if int(close) == 0:
                                    break
                                else:
                                    continue
                            else:
                                continue
                    case 2:
                        while True:
                            tools.clear_terminal()
                            print(
                                "\033[1;36m ALUNOS APROVADOS \033[0;0m".center(60, "="))
                            print()
                            count = 0
                            for line in report.all_approved():
                                print(line)
                                count += 1
                            print("\n%d REGISTRO(S) LISTADOS." % count)
                            close = str(
                                input("\n<< PRESSIONE 0 PARA SAIR >> "))
                            if close.isdigit():
                                if int(close) == 0:
                                    break
                                else:
                                    continue
                            else:
                                continue
                    case 3:
                        while True:
                            tools.clear_terminal()
                            print(
                                "\033[1;36m ALUNOS REPROVADOS POR FALTA \033[0;0m".center(60, "="))
                            print()
                            count = 0
                            for line in report.all_failed():
                                print(line)
                                count += 1
                            print("\n%d REGISTRO(S) LISTADOS." % count)
                            close = str(
                                input("\n<< PRESSIONE 0 PARA SAIR >> "))
                            if close.isdigit():
                                if int(close) == 0:
                                    break
                                else:
                                    continue
                            else:
                                continue
                    case 4:
                        while True:
                            tools.clear_terminal()
                            print(
                                "\033[1;36m ALUNO(S) COM MAIOR MÉDIA \033[0;0m".center(60, "="))
                            print()
                            count = 0
                            for line in report.seek_average(group_by="max"):
                                print(line)
                                count += 1
                            print("\n%d REGISTRO(S) LISTADOS." % count)
                            close = str(
                                input("\n<< PRESSIONE 0 PARA SAIR >> "))
                            if close.isdigit():
                                if int(close) == 0:
                                    break
                                else:
                                    continue
                            else:
                                continue
                    case 5:
                        while True:
                            tools.clear_terminal()
                            print(
                                "\033[1;36m ALUNO(S) COM MENOR MÉDIA \033[0;0m".center(60, "="))
                            print()
                            count = 0
                            for line in report.seek_average(group_by="min"):
                                print(line)
                                count += 1
                            print("\n%d REGISTRO(S) LISTADOS." % count)
                            close = str(
                                input("\n<< PRESSIONE 0 PARA SAIR >> "))
                            if close.isdigit():
                                if int(close) == 0:
                                    break
                                else:
                                    continue
                            else:
                                continue
                    case _:
                        print("\n\033[1;91mOPÇÃO INVÁLIDA\033[0;0m")
                        sleep(1)
            except ValueError:
                print("\n\033[1;91mOPÇÃO INVÁLIDA\033[0;0m")
                sleep(1)

        case 5:
            tools.clear_terminal()
            print("\033[1;36m CADASTRAR MATÉRIA \033[0;0m".center(60, "="))
            try:
                print()
                matter: str = str(
                    input("Nome da disciplina >>> ")).strip().upper()
                teacher: str = str(
                    input("Nome completo do professor >>> ")).strip().upper()
                if not Validator.validate_field_name(teacher):
                    print("""
                    \n\033[1;91m>> PREENCHIMENTO DO CAMPO NOME INVÁLIDO\033[0;0m
                    """.strip("\t"))
                    sleep(1.5)
                    return
                workload: int = int(input("Carga horária >>> "))
                year: str = str(input("Ano >>> ")
                                ).strip().upper()
                insert = settings.insert_settings(
                    matter=matter,
                    teacher=teacher,
                    workload=workload,
                    year=year
                )
                print(insert)
                sleep(1.5)
            except ValueError:
                print("\n\033[1;91m>> DADO INVÁLIDO\033[0;0m")
                sleep(1.5)

        case 6:
            print("\n\n\033[1;31mENCERRANDO APLICAÇÃO...\033[0;0m")
            sleep(1.1)
            sys.exit(1)


def main():
    try:
        while True:
            tools.clear_terminal()
            tools.menu()
            try:
                option = int(input(">>> "))
            except ValueError:
                print("\033[1;91m\nOPÇÃO INVÁLIDA\033[0;0m")
                sleep(1)
            else:
                if option > 6 or option < 1:
                    print("\n\033[1;91mOPÇÃO INVÁLIDA\033[0;0m")
                    sleep(1)
                else:
                    operation(option)
    except KeyboardInterrupt:
        print("\n\n\033[1;31mENCERRANDO APLICAÇÃO...\033[0;0m")
        sleep(1)
        sys.exit(1)


if __name__ == "__main__":
    main()
