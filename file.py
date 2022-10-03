from dataclasses import dataclass
from typing import Generator, Callable
from pathlib import Path
import sys


@dataclass
class File:
    file_name: str
    BASE_DIR: Path = Path(__file__).parent
    FILE_PATH: Path = BASE_DIR / 'data'

    def create(self) -> None:
        with open(self.FILE_PATH / self.file_name, 'w') as f:
            f.write("")

    def read(self) -> list[str]:
        try:
            with open(self.FILE_PATH / self.file_name, "r") as f:
                f.flush()
                return f.readlines()
        except FileNotFoundError:
            sys.exit(1)

    def check(self) -> bool:
        read_file = self.read()
        if not read_file:
            return False
        return True

    def insert_student(self, name: str, gender: str, av: tuple[float], absences: int, func: Callable) -> str:
        if self.file_name == "alunos.txt":
            try:
                extracted_data = func(
                    name,
                    gender,
                    av,
                    absences
                )
                with open(self.FILE_PATH / self.file_name, "a") as f:
                    f.write("%s\n" % extracted_data.strip())
                    return "\n\033[1;92m>> CADASTRO FEITO\033[0;0m"
            except:
                return "\n\033[1;91m>> ERRO AO INSERIR\033[0;0m"
        return "\n\033[1;91m>> MÉTODO NÃO PERTINENTE A ESTE ARQUIVO\033[0;0m"

    def insert_settings(self, matter: str, teacher: str, workload: int, year: str) -> None:
        if self.file_name == "materia.txt":
            try:
                with open(self.FILE_PATH / self.file_name, "w") as f:
                    f.write("{};{};{};{}\n".format(
                        matter,
                        teacher,
                        workload,
                        year
                    ))
                return "\n\033[1;92m>> CADASTRO FEITO\033[0;0m"
            except:
                return "\n\033[1;91m>> ERRO AO INSERIR\033[0;0m"
        else:
            return "\n\033[1;91m>> MÉTODO NÃO PERTINENTE A ESTE ARQUIVO\033[0;0m"

    def delete(self, index: int) -> str:
        read_file = self.read()
        data = (line.strip("\n") for line in read_file)  # expressão geradora
        ptr = 1
        with open(self.FILE_PATH / self.file_name, "w") as f:
            try:
                for line in data:
                    if ptr != index:
                        f.write(line + "\n")
                    if ptr == index:
                        line_deleted = line
                    ptr += 1
                return "\n\033[1;32m>> DELETADO ->\033[0;0m %s" % line_deleted
            except UnboundLocalError:
                return "\n\033[1;91m>> ÍNDICE INVÁLIDO\033[0;0m"

    def search(self, cod: int) -> str:
        read_file = self.read()
        get_line = None
        for index, line in enumerate(read_file, start=1):
            query = line.strip("\n").split(";")
            if query[0][-12:] == str(cod):
                get_line = query
        if not get_line:
            return "\n\033[1;93m>> NÃO ENCONTRADO\033[0;0m"
        return f"""
        {index} - MATERIA: {get_line[0]}
        NOME: {get_line[1]}
        SEXO: {get_line[2]}
        NOTAS: {get_line[3]}
        MEDIA: {get_line[4]}
        FALTAS: {get_line[5]}
        """


@dataclass
class Report:
    def inner_join(self) -> Generator:
        f1 = [data.strip().split(";") for data in open("./data/alunos.txt")]
        f2 = [data.strip().split(";") for data in open("./data/materia.txt")]
        if not f2:
            f2 = [["---", "---", "---", "---"]]
        for line in f1:
            yield line + f2[0]

    def all_lines(self) -> Generator:
        data = self.inner_join()
        for index, line in enumerate(data, start=1):
            if "---" in line[5] or "---" in line[8]:
                if float(line[4]) >= 6:
                    situation = "\033[1;92mAPROVADO\033[0;0m"
                else:
                    situation = "\033[1;91mREPROVADO\033[0;0m"
                yield f"""
        {index} - MATRICULA: {line[0]}
        NOME: {line[1]}
        SEXO: {line[2]}
        NOTAS:{line[3]}
        MEDIA: {line[4]}
        FALTAS: {line[5]}
        FREQUENCIA: ---
        MATERIA: {line[6]}
        PROFESSOR: {line[7]}
        CARGA HORARIA: {line[8]}
        ANO: {line[9]}
        SITUAÇAO: {situation}
                """
            else:
                ch = int(line[8])
                absences = int(line[5])
                frequency = round((ch - absences) / ch * 100)
                if float(line[4]) >= 6.0 and frequency >= 75:
                    situation = "\033[1;92mAPROVADO\033[0;0m"
                else:
                    situation = "\033[1;91mREPROVADO\033[0;0m"
                yield f"""
        {index} - MATRICULA: {line[0]}
        NOME: {line[1]}
        SEXO: {line[2]}
        NOTAS:{line[3]}
        MEDIA: {line[4]}
        FALTAS: {line[5]}
        FREQUENCIA: {str(frequency) + "%"}
        MATERIA: {line[6]}
        PROFESSOR: {line[7]}
        CARGA HORARIA: {line[8]} HORAS
        ANO: {line[9]}
        SITUACAO: {situation}
            """

    def all_approved(self) -> Generator:
        data = self.inner_join()
        for index, line in enumerate(data, start=1):
            if "---" in line[5] or "---" in line[8]:
                if float(line[4]) >= 6:
                    situation = "\033[1;92mAPROVADO\033[0;0m"
                    yield f"""
        {index} - MATRICULA: {line[0]}
        NOME: {line[1]}
        SEXO: {line[2]}
        NOTAS:{line[3]}
        MEDIA: {line[4]}
        FALTAS: {line[5]}
        FREQUENCIA: ---
        MATERIA: {line[6]}
        PROFESSOR: {line[7]}
        CARGA HORARIA: {line[8]}
        ANO: {line[9]}
        SITUAÇAO: {situation}
                """
            else:
                ch = int(line[8])
                absences = int(line[5])
                frequency = round((ch - absences) / ch * 100)
                if float(line[4]) >= 6.0 and frequency >= 75:
                    situation = "\033[1;92mAPROVADO\033[0;0m"
                    yield f"""
        {index} - MATRICULA: {line[0]}
        NOME: {line[1]}
        SEXO: {line[2]}
        NOTAS:{line[3]}
        MEDIA: {line[4]}
        FALTAS: {line[5]}
        FREQUENCIA: {str(frequency) + "%"}
        MATERIA: {line[6]}
        PROFESSOR: {line[7]}
        CARGA HORARIA: {line[8]} HORAS
        ANO: {line[9]}
        SITUACAO: {situation}
                """

    def all_failed(self) -> Generator:
        data = self.inner_join()
        for index, line in enumerate(data, start=1):
            if "---" in line[5] or "---" in line[8]:
                pass
            else:
                ch = int(line[8])
                absences = int(line[5])
                frequency = round((ch - absences) / ch * 100)
                if frequency < 75:
                    situation = "\033[1;91mREPROVADO\033[0;0m"
                    yield f"""  
        {index} - MATRICULA: {line[0]}
        NOME: {line[1]}
        SEXO: {line[2]}
        NOTAS:{line[3]}
        MEDIA: {line[4]}
        FALTAS: {line[5]}
        FREQUENCIA: {str(frequency) + "%"}
        MATERIA: {line[6]}
        PROFESSOR: {line[7]}
        CARGA HORARIA: {line[8]} HORAS
        ANO: {line[9]}
        SITUACAO: {situation}
                """

    def get_value(self, group_by: str) -> float:
        data = self.inner_join()
        get_avg = [float(avg[4]) for avg in data]
        if not get_avg:
            return None
        if group_by == "max":
            return max(get_avg)
        if group_by == "min":
            return min(get_avg)

    def seek_average(self, group_by: str = "max") -> Generator:
        data = self.inner_join()
        avg = self.get_value(group_by)
        if not avg:
            return
        for index, line in enumerate(data, start=1):
            if "---" in line[5] or "---" in line[8]:
                if float(line[4]) >= 6:
                    situation = "\033[1;92mAPROVADO\033[0;0m"
                else:
                    situation = "\033[1;91mREPROVADO\033[0;0m"
                if avg == float(line[4]):
                    yield f"""
        {index} - MATRICULA: {line[0]}
        NOME: {line[1]}
        SEXO: {line[2]}
        NOTAS:{line[3]}
        MEDIA: {line[4]}
        FALTAS: {line[5]}
        FREQUENCIA: ---
        MATERIA: {line[6]}
        PROFESSOR: {line[7]}
        CARGA HORARIA: {line[8]}
        ANO: {line[9]}
        SITUAÇAO: {situation}
                    """
            else:
                ch = int(line[8])
                absences = int(line[5])
                frequency = round((ch - absences) / ch * 100)
                if float(line[4]) >= 6.0 and frequency >= 75:
                    situation = "\033[1;92mAPROVADO\033[0;0m"
                else:
                    situation = "\033[1;91mREPROVADO\033[0;0m"
                if avg == float(line[4]):
                    yield f"""
        {index} - MATRICULA: {line[0]}
        NOME: {line[1]}
        SEXO: {line[2]}
        NOTAS:{line[3]}
        MEDIA: {line[4]}
        FALTAS: {line[5]}
        FREQUENCIA: {str(frequency) + "%"}
        MATERIA: {line[6]}
        PROFESSOR: {line[7]}
        CARGA HORARIA: {line[8]} HORAS
        ANO: {line[9]}
        SITUACAO: {situation}
        """
