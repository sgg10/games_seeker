import re
from itertools import product
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


class CPUException(Exception):
    pass


class Improver:

    def __init__(self):
        self.regexs = {
            "cpu": r"([3-9])-(\d{1,2})-([UBHKZX])"
        }

        self.CPU = {
            "model": {m: (33.33 / 4) * (idx + 1) for idx, m in enumerate((3, 5, 7, 9))},
            "generation": {g: (33.33 / 8) * (idx + 1) for idx, g in enumerate(range(5, 13))},
            "serie": {s: (33.33 / 6) * (idx + 1) for idx, s in enumerate(("U", "B", "H", "K", "Z", "X"))}
        }

        self.RAM = {
            ram: round((100 / 11) * (idx+1), 4)
            for idx, ram in enumerate((2, 4, 6, 8, 10, 12, 16, 24, 32, 64, 128))
        }

        self.cpu, self.improve_cpu, self.ram, self.improve_ram = self.init_components()

        self.speed_improver, self.performance_improver = self.create_controllers(*self.get_rules())

    def init_components(self):
        cpu = ctrl.Antecedent(np.arange(0, 101, 1), 'cpu')
        ram = ctrl.Antecedent(np.arange(0, 101, 1), 'ram')

        cpu.automf(3)
        ram.automf(3)

        improve_cpu = ctrl.Consequent(np.arange(0, 100, 1), 'improve_cpu')
        improve_cpu['low'] = fuzz.trimf(improve_cpu.universe, [0, 0, 33])
        improve_cpu['medium'] = fuzz.trimf(improve_cpu.universe, [0, 33, 66])
        improve_cpu['high'] = fuzz.trimf(improve_cpu.universe, [33, 66, 100])

        improve_ram = ctrl.Consequent(np.arange(0, 100, 1), 'improve_ram')
        improve_ram['low'] = fuzz.trimf(improve_ram.universe, [0, 0, 33])
        improve_ram['medium'] = fuzz.trimf(improve_ram.universe, [0, 33, 66])
        improve_ram['high'] = fuzz.trimf(improve_ram.universe, [33, 66, 100])

        return cpu, improve_cpu, ram, improve_ram

    def get_rules(self):
        speed_rules = [
            ctrl.Rule(self.cpu["poor"] & self.ram["poor"], self.improve_ram["low"]),
            ctrl.Rule(self.cpu["average"] & self.ram["poor"], self.improve_ram["medium"]),
            ctrl.Rule(self.cpu["good"] & self.ram["poor"], self.improve_ram["medium"]),
            ctrl.Rule(self.cpu["average"], self.improve_ram["high"]),
            ctrl.Rule(self.cpu["average"] & self.ram["average"], self.improve_ram["high"]),
            ctrl.Rule(self.cpu["good"] & self.ram["average"], self.improve_ram["high"]),
            ctrl.Rule(self.cpu["good"] & self.ram["good"], self.improve_ram["high"]),
        ]
        performance_rules = [
            ctrl.Rule(self.cpu["poor"] & self.ram["poor"], self.improve_cpu["medium"]),
            ctrl.Rule(self.cpu["poor"] & self.ram["average"], self.improve_cpu["medium"]),
            ctrl.Rule(self.cpu["average"] & self.ram["average"], self.improve_cpu["high"]),
            ctrl.Rule(self.cpu["good"] & self.ram["average"], self.improve_cpu["high"]),
            ctrl.Rule(self.cpu["good"] & self.ram["good"], self.improve_cpu["high"]),
            ctrl.Rule(self.cpu["good"], self.improve_cpu["high"]),
            ctrl.Rule(self.ram["good"], self.improve_cpu["high"]),
        ]

        return speed_rules, performance_rules

    def create_controllers(self, speed_rules, performance_rules):
        speed_ctrl = ctrl.ControlSystem(speed_rules)
        speed_improver = ctrl.ControlSystemSimulation(speed_ctrl)
        performance_ctrl = ctrl.ControlSystem(performance_rules)
        performance_improver = ctrl.ControlSystemSimulation(performance_ctrl)

        return speed_improver, performance_improver

    def query(self, cpu, ram, query_type):
        if re.search(self.regexs["cpu"], cpu):
            cpu, cpu_gen, cpu_serie = re.search(self.regexs["cpu"], cpu).groups()
            calculated_cpu = (
                    self.CPU["model"][int(cpu)] + self.CPU["generation"][int(cpu_gen)] + self.CPU["serie"][cpu_serie]
            )
        else:
            raise CPUException(f"Invalid CPU: {cpu}")

        improver = self.speed_improver if query_type == "speed" else self.performance_improver

        improver.inputs(
            {
                "cpu": calculated_cpu,
                "ram": self.RAM[int(ram)]
            }
        )

        improver.compute()

        if query_type == "speed":
            ranges = (
                (9.0909, 18.1817, 2),
                (18.1818, 27.2726, 4),
                (27.2727, 36.3635, 6),
                (36.3636, 45.4544, 8),
                (45.4545, 54.5454, 10),
                (54.5455, 63.6363, 12),
                (63.6364, 72.7272, 16),
                (72.7273, 81.8181, 24),
                (81.8182, 90.9090, 32),
                (90.9091, 99.9999, 64),
                (100, 100, 128)
            )
            result = improver.output["improve_ram"]
            for low, high, to_improve in ranges:
                if low <= result <= high:
                    suggest_ram = to_improve
                    break

            message = f"Le sugerimos tener {suggest_ram} GB de memoria RAM"
        else:
            product_options = list(
                product(self.CPU["model"].keys(), self.CPU["generation"].keys(), self.CPU["serie"].keys())
            )
            result = improver.output["improve_cpu"]
            evaluate_cpu = lambda x: 'low' if x <= 33.33 else 'medium' if 33.33 < x <= 66.66 else 'high'
            range_result = evaluate_cpu(result)

            options = [
                f'{m}-{g}-{s}'
                for m, g, s in product_options
                if self.CPU["model"][m] + self.CPU["generation"][g] + self.CPU["serie"][s] > result
                and range_result == evaluate_cpu(
                    self.CPU["model"][m] + self.CPU["generation"][g] + self.CPU["serie"][s]
                )
            ]
            message = f'Le sugerimos cambiar a uno de los estos procesadores: {options}'

        return message
