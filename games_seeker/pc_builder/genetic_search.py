import random
from time import time

import click
import numpy as np
import pandas as pd

from deap import algorithms, base, creator, tools


class GeneticSearch:
    COMPONENTS_ORDER = ("CPU", "Mother Board", "RAM", "Storage", "GPU", "Refrigeration", "Power Supply", "Chasis")
    PRODUCT_INFO = ["title", "type", "price", "link"]

    def __init__(self, budget):
        self.PRODUCTS = pd.read_csv("data/interim/pc_components.csv", sep="|", encoding="utf-8")
        self.budget = budget
        self.toolbox = None

    def create_individual(self):
        return [
            random.choice(self.PRODUCTS[self.PRODUCTS["type"] == product].index)
            for product in self.COMPONENTS_ORDER
        ]

    def evaluate_budget(self, individual):
        prices = [self.PRODUCTS.loc[idx, "price"] for idx in individual]
        total = sum(prices)
        _, counts = np.unique(individual, return_counts=True)
        if not all(counts == 1):
            return -1,
        return (total,) if total <= self.budget else (-1,)

    def register_initial_components(self):
        for _class in ("FitnessMax", "Individual"):
            if _class in dir(creator):
                delattr(creator, _class)

        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMax)

        self.toolbox = base.Toolbox()

        self.toolbox.register("indices", self.create_individual)
        self.toolbox.register("individual", tools.initIterate, creator.Individual, self.toolbox.indices)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)

    def register_genetic_operators(self):
        self.toolbox.register("mate", tools.cxOnePoint)
        self.toolbox.register("mutate", tools.mutFlipBit, indpb=0.1)
        self.toolbox.register("select", tools.selTournament, tournsize=3)
        self.toolbox.register("evaluate", self.evaluate_budget)

    def _run_evaluation(self, CXPB, MUTPB, NGEN, NIND=50, verbose=False, **kwargs):
        pop = self.toolbox.population(NIND)
        hof = tools.HallOfFame(1)

        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", np.mean)
        stats.register("std", np.std)
        stats.register("min", np.min)
        stats.register("max", np.max)

        pop, logbook = algorithms.eaSimple(
            pop,
            self.toolbox,
            CXPB,
            MUTPB,
            NGEN,
            stats=stats,
            halloffame=hof,
            verbose=verbose
        )
        return pop, logbook

    def run(self, cases, config):
        random.seed(100)
        results = []
        results_logs = {idx + 1: [] for idx in range(len(cases))}
        for idx, case in enumerate(cases):
            self.register_initial_components()
            self.register_genetic_operators()

            with click.progressbar(range(config["iterations"] + 1), label=f"Searching with configuration {idx+1}") as b:
                for i in b:
                    t0 = time()
                    best, log = self._run_evaluation(**case)
                    results.append(
                        [
                            idx + 1, i, case["NIND"], case["CXPB"],
                            case["MUTPB"], case["NGEN"], best[0].fitness.values[0],
                            best[0], round(time() - t0, 4)
                        ]
                    )
                    results_logs[idx + 1].append(log)

        results = pd.DataFrame(
            results,
            columns=["Test ID", "Try", "Population", "CXPB", "MUTPB", "NGEN", "Best Fitness", "Best", "Time"]
        )
        results = results[results["Best Fitness"] > 0]
        results.sort_values(by=["Best Fitness"], axis=0, ascending=False, inplace=True)

        return results, results_logs
