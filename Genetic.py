import math
import types
import warnings
import random

class Genome:
    mutationTries = 20
    mutationChance = 0.05
    def __init__(self, prob, sol=None):
        self.prob = prob
        self.fitness = 0
    def initialize(self, rand=True):
        pass
    def cross(self, gen2):
        pass
    def mutate(self):
        pass
    def testFitness(self):
        self.fitness = self.prob.getScore(self.solution)
        return self.fitness


class Problem:
    def getScore(self, input):
        pass
    def createRandomSolution(self, input):
        pass


class Genetic:
    def __init__(self, prob, genomeClass, popSize = 100, carryOn = 10):
        self.problem = prob
        self.popSize = popSize
        self.carryOn = carryOn
        self.GenomeClass = genomeClass
        self.population = []
        self.levels = []
    def createPopulation(self):
        self.population = [self.GenomeClass(self.problem) for _ in range(self.popSize)]
        for i in self.population:
            i.initialize()
    def testFitness(self):
        for org in self.population:
            org.testFitness()
        self.population = sorted(self.population, key=lambda x : x.fitness)
    def selectRandomWeighted(arr, W):
        S = sum(W)
        mx = random.random()*S
        #print(mx, S)
        for i in range(len(arr)):
            if mx < W[i]:
                return arr[i]
            mx -= W[i]
        assert False,"selectRandom() went to the end" 
    def selectRandom(self):
        return Genetic.selectRandomWeighted(self.population, range(self.popSize))
    
    def nextGeneration(self):
        next = []
        while len(next) < (self.popSize-self.carryOn):
            g1 = self.selectRandom()
            g2 = self.selectRandom()
            o1, o2 = g1.cross(g2)
            o1.mutate()
            o2.mutate()
            next.append(o1)
            next.append(o2)
        while len(next) > self.popSize-self.carryOn:
            next.pop(self.popSize-self.carryOn)
        for i in range(self.carryOn):
            next.append(self.population[len(self.population)-1-i])
        self.levels.append(self.population)
        self.population = next
    def advanceGenerations(self, gen):
        for i in range(gen):
            self.testFitness()
            self.nextGeneration()