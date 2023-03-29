import random
from random import randint, sample

file_array = open('array.txt', 'r')
len_people = 10
nlines, ncolumns = file_array.readline().split()
lines = file_array.read().splitlines()

coords = {}
send_points = []

for i in range(int(nlines)):
    line = lines[i].split()
    for j in line:
        if j != '0':
            coords[j] = (i, line.index(j))
            send_points.append(j)



def generate_people(DeliveryPoints):
    population = [i for i in DeliveryPoints if i!='R']
    pop_initial = []
    i = 0
    while i != len_people:
        ip = sample(population, len(population))
        if ip not in pop_initial:
            pop_initial.append(ip)
            i += 1
    return pop_initial


def fitness(route):
    n = 0
    coust_route = 0
    route.append('R')
    route.insert(0, 'R')

    while n < len(route)-1:
        y = abs(coords[route[n]][0] - coords[route[n+1]][0])
        x = abs(coords[route[n]][1] - coords[route[n+1]][1])
        coust_route += x + y
        n += 1

    del(route[0], route[-1])

    return coust_route


def rank(population):
    population.sort(key=lambda x:x[0])
    return population

def selection(population, n1, n2):
    more = []
    torneio = []
    for i in range(n1):
        compet = random.sample(population, n2)
        for j in compet:
            torneio.append((fitness(j), j))
        champion = rank(torneio)[0][1]
        more.append(champion)

    return more

def crossover(father, mom):
    breakpoint = randint(1, len(father)-1)
    copy = mom[:]
    childrens = []

    for children in range(2):
        for point in range(breakpoint):
            if father[point] != mom[point]:
                temp = mom[point]
                mom[point] = father[point]

                for change_point in range(point+1, len(mom)):
                    if mom[point] == mom[change_point]:
                        mom[change_point] = temp
                        break
        
        childrens.append(mom)
        mom = father
        father = copy

    return childrens

def mutation(routes):
    if random.random() < 0.07:
        mutation_point = randint(0, len(routes)-2)
        copy = routes[mutation_point]

        routes[mutation_point] = routes[mutation_point+1]
        routes[mutation_point+1] = copy

        return routes

def main(total):
    population = generate_people(send_points)
    best_coust = float('inf')
    geracoes = 0
    more_b_coust = 0

    while geracoes < total:
        selecao = selection(population, 20, 5)
        populacao = []
        for a in range(50):
            father = random.choice(selecao)
            mom = random.choice(selecao)

            son1, son2 = crossover(father, mom)

            mutation(son1)
            mutation(son2)

            populacao.append(son1)
            populacao.append(son2)

        geracoes += 1

        solucao_otima = selection(populacao, 1, 100)[0]

        if fitness(solucao_otima) < best_coust:
            best_coust = fitness(solucao_otima)
            more_b_coust = best_coust
            best_route = solucao_otima

    return best_route, more_b_coust


result = main(100)
print(f"A melhor rota é {result[0]}, que custa {result[1]}") 
