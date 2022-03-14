import ast
import pandas as pd
import pytholog as pl
import numpy as np

class Logic:

    def __init__(self):
        self.GAMES_REQUIREMENTS = pd.read_csv("data/interim/games_requirements.csv", sep="|")
        self.GAMES_REQUIREMENTS.loc[:, "Procesador"] = self.GAMES_REQUIREMENTS.loc[:, "Procesador"].apply(
            lambda x: ast.literal_eval(x)
        )
        self.GAMES_REQUIREMENTS.loc[:, "Gráficos"] = self.GAMES_REQUIREMENTS.loc[:, "Gráficos"].apply(
            lambda x: ast.literal_eval(x)
        )

        self.games_kb = pl.KnowledgeBase("games")
        self.games_kb(self.create_knowledge_base())

    def create_knowledge_base(self):
        facts = []

        # Equivalencia
        tmp = [f"equivale(i{n},r{n})" for n in range(3, 10, 2)]
        tmp += [f"equivale({marca}{n},{marca}{n})" for marca in ["i", "r"] for n in range(3, 10, 2)]
        tmp += [f"equivale({marca}{n},{marca}{n})" for marca in ["r", "i"] for n in range(3, 10, 2)]

        facts += list(set(tmp))

        # Superioridad
        tmp = [
            f"superioridad({marca}{n_s},{marca}{n_i})"
            for marca in ["i", "r"]
            for n_s in range(9, 2, -2)
            for n_i in range(3, 10, 2)
            if n_s > n_i
        ]

        facts += list(set(tmp))

        # Requisitos minimos
        for game in self.GAMES_REQUIREMENTS.values:
            tmp = []
            for cpu in game[3]:
                for gpu in game[5]:
                    tmp.append(f"requerimiento({game[0]},{game[2]},{cpu},{game[4]},{gpu},{game[6]})")
            facts += list(set(tmp))

        # Reglas
        facts.append("valSO(X,Y) :- X >= Y")
        facts.append("valRAM(X,Y) :- X >= Y")
        facts.append("valStorage(X,Y) :- X >= Y")
        facts.append("valGPU(X,Y) :- X >= Y")

        facts.append("superior(X,Y) :- equivale(Y,Z),superioridad(X,Z);superioridad(X,Z)")
        facts.append("puede_jugar(NAME,B,C,X,Y,Z) :- requerimiento(NAME,SO,CPU,RAM,GPU,STO)")
        facts.append(
            "puede_jugar(SO,I_SO,CPU,I_CPU,RAM,I_RAM,GPU,I_GPU,STO,I_STO) :- valSO(SO,I_SO),equivale(CPU,I_CPU),"
            "valRAM(RAM,I_RAM),valGPU(GPU,I_GPU),valStorage(STO,I_STO)"
        )
        facts.append(
            "puede_jugar(SO,I_SO,CPU,I_CPU,RAM,I_RAM,GPU,I_GPU,STO,I_STO) :- valSO(SO,I_SO),superior(CPU,I_CPU),"
            "valRAM(RAM,I_RAM),valGPU(GPU,I_GPU),valStorage(STO,I_STO)"
        )

        return facts

    def can_run_game(self, name, so, cpu, ram, gpu, st):
        g_filter = self.GAMES_REQUIREMENTS["name"] == name
        g_name, _, g_so, g_cpu, g_ram, g_gpu, g_st = self.GAMES_REQUIREMENTS[g_filter].values[0]
        result = self.games_kb.query(pl.Expr(f"requerimiento({name},{so},{cpu},{ram},{gpu},{st})"))[0]
        if result == "No":
            result = self.games_kb.query(
                pl.Expr(f"puede_jugar({so},{g_so},{cpu},{g_cpu[0]},{ram},{g_ram},{gpu},{g_gpu[0]},{st},{g_st})")
            )[0]
        return True if result == "Yes" else False

