import re
from pickle import load

"""from sklearn import tree
from sklearn import preprocessing
"""


class CPUException(Exception):
    pass


class GPUException(Exception):
    pass


class PCClassifier:

    def __init__(self):
        self.model = load(open("./models/model.pkl", "rb"))
        self.encoders = {
            "cpu_series": load(open("./models/cpu_serie_encoder.pkl", "rb"))
        }
        self.targets = {0: "Diseño", 1: "Gamer", 2: "Ofimatica"}
        self.regexs = {
            "cpu": r"([3-9])-(\d{1})-([QBUHZ])",
            "gpu": r"((?:-1|(?:10|20|30)(?:30|40|50|60|70|80)))(-TI){0,1}"
        }

    def query(self, cpu, ram, gpu, hdd, ssd):
        if re.search(self.regexs["cpu"], cpu):
            cpu, cpu_gen, cpu_serie = re.search(self.regexs["cpu"], cpu).groups()
            cpu_serie = self.encoders["cpu_series"].transform([cpu_serie])[0]
        else:
            raise CPUException(f"Invalid CPU: {cpu}")

        if re.search(self.regexs["gpu"], gpu):
            gpu, is_ti = re.search(self.regexs["gpu"], gpu).groups()
            is_ti = 1 if is_ti else 0
        else:
            raise GPUException(f"Invalid GPU: {gpu}")

        result = self.model.predict([
            [int(cpu), int(cpu_gen), int(cpu_serie), int(ram), int(gpu), int(is_ti), int(hdd), int(ssd)]
        ])

        return f"La configuración seleccionada corresponde a un PC de tipo: {self.targets[result[0]]}"
