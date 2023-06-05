import networkx as nx
import matplotlib.pyplot as plt
import random
import io
from PIL import Image


class max_clique_finder:
    @staticmethod
    def find(path):
        NUMBER_NODES = -1
        NUMBER_EDGES = -1
        POPULATION = 10
        LOCAL_IMPROVEMENT = 10
        GENERATIONS = 100
        MUTATIONS = 1
        UNIQUE_ITERATIONS = 100
        SHUFFLE_TOLERANCE = 10
        Graph = nx.Graph()

        class Clique:
            def __init__(self, first_vertex=-1):
                self.clique = []
                self.pa = []
                self.dict_pa = {}
                self.dict_clique = {}
                if first_vertex != -1:
                    self.clique.append(first_vertex)
                    self.dict_clique[first_vertex] = True
                    for node in list(Graph.nodes):
                        if node == first_vertex:
                            continue
                        else:
                            if Graph.has_edge(node, first_vertex):
                                # print('Должна быть добавлена ПА')
                                self.pa.append(node)
                                self.dict_pa[node] = True

            def add_vertex(self, vertex):
                if vertex in self.clique:
                    return
                self.clique.append(vertex)
                self.dict_clique[vertex] = True
                self.erase_from_pa(vertex)
                erased_nodes = []
                for n in self.pa:
                    if not Graph.has_edge(n, vertex):
                        erased_nodes.append(n)
                for n in erased_nodes:
                    self.erase_from_pa(n)

            def remove_vertex(self, vertex):
                if not (vertex in self.clique):
                    return
                self.erase_from_clique(vertex)
                for node in Graph.nodes:
                    if node in self.clique:
                        continue
                    else:
                        flag = True
                    for n_c in self.clique:
                        if not Graph.has_edge(node, n_c):
                            flag = False
                            break
                    if flag:
                        if not node in self.pa:
                            self.pa.append(node)
                            self.dict_pa[node] = True

            def erase_from_pa(self, vertex):
                self.dict_pa.pop(vertex)
                flag = False
                a = 0
                for a in self.pa:
                    # print('a - ', a)
                    if a == vertex:
                        flag = True
                        break
                if flag:
                    self.pa.remove(a)

            def erase_from_clique(self, vertex):
                self.dict_clique.pop(vertex)
                flag = False
                n = 0
                for n in self.clique:
                    if n == vertex:
                        flag = True
                        break
                if flag:
                    self.clique.remove(n)

            def compute_sorted_by_degree(self):
                sorted_list = []
                for node1 in self.pa:
                    reach = 0
                    for node2 in self.pa:
                        if node1 == node2:
                            continue
                        if Graph.has_edge(node1, node2):
                            reach += 1
                    sorted_list.append((node1, reach))
                sorted_list = sorted(sorted_list, key=lambda x: x[1], reverse=True)
                return list(map(lambda x: x[0], sorted_list))
                # degrees = Graph.degree(self.clique)
                # degrees = sorted(degrees, key=lambda x: x[1], reverse=True)
                # return list(map(lambda x: [0], degrees))

            def clone(self):
                cpa = []
                cclique = []
                cdict_pa = {}
                cdict_clique = {}
                for a in self.pa:
                    cpa.append(a)
                for cl in self.clique:
                    cclique.append(cl)
                for key in self.dict_pa.keys():
                    cdict_pa[key] = self.dict_pa[key]
                for key in self.dict_clique.keys():
                    cdict_clique[key] = self.dict_clique[key]
                clique_clone = Clique()
                clique_clone.pa = cpa
                clique_clone.clique = cclique
                clique_clone.dict_pa = cdict_pa
                clique_clone.dict_clique = cdict_clique
                return clique_clone

        def generate_random_population():
            print("Generating population...")
            population = []
            flags = NUMBER_NODES * [False]
            for pop in range(POPULATION):
                rand = random.randint(0, NUMBER_NODES - 1)
                cntt = 0
                while flags[rand]:
                    if cntt > NUMBER_NODES:
                        print('брейкнулся')
                        break
                    # print("крутимся")
                    rand = random.randint(0, NUMBER_NODES - 1)
                flags[rand] = True
                clique = Clique(rand)
                # print('ПА клики', clique.pa)
                sortedList = clique.compute_sorted_by_degree()

                cnt = 0
                while len(clique.pa) > 0:
                    # print("PA - ", clique.pa)
                    node = sortedList[cnt]
                    cnt += 1
                    if node in clique.pa:
                        clique.add_vertex(node)
                # print('Особь -', clique.clique)
                population.append(clique)
            return population

        def greedy_crossover(clique1, clique2):
            vec = []
            flags = NUMBER_NODES * [False]
            for vertex in clique1.clique:
                if not flags[vertex]:
                    vec.append(vertex)
                    flags[vertex] = True
            for vertex in clique2.clique:
                if not flags[vertex]:
                    vec.append(vertex)
                    flags[vertex] = True

            cliques_nodes_degrees_sort = []
            for node1 in vec:
                reach = 0
                for node2 in vec:
                    if Graph.has_edge(node1, node2):
                        reach += 1
                cliques_nodes_degrees_sort.append((node1, reach))
            sorted(cliques_nodes_degrees_sort, key=lambda x: x[1])
            firstVertex = cliques_nodes_degrees_sort[0][0]
            clique = Clique(firstVertex)
            count = 1
            while count < len(cliques_nodes_degrees_sort):
                node = cliques_nodes_degrees_sort[0]
                if node in clique.pa:
                    clique.add_vertex(node)
                count += 1
            while len(clique.pa) > 0:
                node = clique.pa[0]
                clique.add_vertex(node)
            return clique

        def intersection_crossover(clique1, clique2):
            intersect = []
            print(NUMBER_NODES)
            flags = NUMBER_NODES * [False]

            for ver in clique2.clique:
                flags[ver] = True

            for ver in clique1.clique:
                if flags[ver]:
                    intersect.append(ver)
            if len(intersect) == 0:
                return greedy_crossover(clique1, clique2)

            vertex = intersect[0]
            clique = Clique(vertex)
            for vertex in intersect:
                if vertex in clique.pa:
                    clique.add_vertex(vertex)

            if len(clique.pa) > 0:
                sorted_clique_list = clique.compute_sorted_by_degree()
                cnt = 0
                while len(clique.pa) > 0:
                    node = sorted_clique_list[cnt]
                    cnt += 1
                    if node in clique.pa:
                        clique.add_vertex(node)
            return clique

        def random_selection(population):
            parents = []
            rand1 = random.randint(0, POPULATION - 1)
            rand2 = random.randint(0, POPULATION - 1)
            while (rand1 == rand2):
                rand1 = random.randint(0, POPULATION - 1)
                rand2 = random.randint(0, POPULATION - 1)

            p1 = population[rand1]
            p2 = population[rand2]
            parents.append(p1)
            parents.append(p2)
            return parents

        def local_improvement(clique):
            g_best = clique.clone()
            for i in range(LOCAL_IMPROVEMENT):
                rand1 = random.randint(0, len(clique.clique) - 1)
                rand2 = random.randint(0, len(clique.clique) - 1)
                countt = 0
                while rand1 == rand2:
                    countt += 1
                    if countt > UNIQUE_ITERATIONS:
                        break
                    rand1 = random.randint(0, len(clique.clique) - 1)
                    rand2 = random.randint(0, len(clique.clique) - 1)
                vertex1 = clique.clique[rand1]
                vertex2 = clique.clique[rand2]
                clique.remove_vertex(vertex1)
                clique.remove_vertex(vertex2)
                sorted_list = clique.compute_sorted_by_degree()
                count = 0
                while len(clique.pa) > 0:
                    node = sorted_list[count]
                    count += 1
                    if node >= NUMBER_NODES:
                        print("ЧТО-ТО ОЧЕНЬ ДЕРЬМОВО")
                    if node in clique.pa:
                        clique.add_vertex(node)
                if len(g_best.clique) < len(clique.clique):
                    g_best = clique.clone()
            clique = g_best

        def mutate(clique):
            flags = NUMBER_NODES * [False]
            for i in range(MUTATIONS):
                rand = random.randint(0, len(clique.clique) - 1)
                count = 0
                while flags[rand]:
                    rand = random.randint(0, len(clique.clique) - 1)
                    count += 1
                    if count > UNIQUE_ITERATIONS:
                        break
                flags[rand] = True
                vertex = clique.clique[rand]
                clique.remove_vertex(vertex)
            rand = random.uniform(0.0, 1.0)
            if rand < 0.5:
                sortedList = clique.compute_sorted_by_degree()
                cnt = 0
                while len(clique.pa) > 0:
                    node = sortedList[cnt]
                    cnt += 1
                    if node in clique.pa:
                        clique.add_vertex(node)
            else:
                while len(clique.pa) > 0:
                    rand = random.randint(0, len(clique.pa) - 1)
                    vertex = clique.pa[rand]
                    clique.add_vertex(vertex)


        f = open(path, 'r')

        for line in f:
            s = line.split()
            # print(s)
            if len(s) > 1:
                Graph.add_edge(int(s[1]), int(s[2]))
            else:
                Graph.add_node(int(s[1]))
        NUMBER_NODES = len(Graph.nodes)
        NUMBER_EDGES = len(Graph.edges)


        population = []
        population = generate_random_population()
        # print("РАЗМЕР ПОПУЛЯЦИИ -", len(population))
        print("Популяция сгенерировалась")
        population = sorted(population, key=lambda x: len(x.clique), reverse=True)
        g_best = population[0].clone()
        prev_best = len(g_best.clique)
        cnt = 0
        # print(228)
        for n in range(GENERATIONS):
            print("Поколение", n)
            if prev_best == len(g_best.clique):
                cnt += 1
                if cnt > SHUFFLE_TOLERANCE:
                    pop = generate_random_population()
                    population = pop.copy()
                    pop.clear()
                    cnt = 0
            else:
                prev_best = len(g_best.clique)
                cnt = 0
            new_population = []
            population = sorted(population, key=lambda x: len(x.clique), reverse=True)

            local_best = population[0]
            print()
            if len(g_best.clique) < len(local_best.clique):
                g_best = local_best.clone()
            print("Глобально лучшая", g_best.clique)
            local_improvement(g_best)
            new_population.append(g_best)

            for i in range(POPULATION - 1):
                print("Популяция ", i)
                parents = random_selection(population)
                # print('родитель 1', parents[0].clique)
                # print('родитель 2', parents[1].clique)
                offspring = intersection_crossover(parents[0], parents[1])
                local_improvement(offspring)
                if len(offspring.clique) <= len(parents[0].clique) or len(offspring.clique) <= len(parents[1].clique):
                    mutate(offspring)
                new_population.append(offspring)
            population = new_population.copy()
            new_population.clear()

        max_clique = g_best.clique
        print("Вершины в клике")
        print(max_clique)

        color_map = []
        for n in Graph.nodes:
            if n in max_clique:
                color_map.append('red')
            else:
                color_map.append('blue')

        im_io = io.BytesIO()
        fig, ax = plt.subplots()
        nx.draw(Graph, node_color=color_map, ax=ax)
        fig.savefig(im_io, format='png')
        im = Image.open(im_io)
        print('image', im)
        clique_answer = {
            'clique': g_best.clique,
            'image': im
        }
        return clique_answer