from merge_sort import merge_sort
from quick_sort import quick_sort
from insertion_sort import insertion_sort
import random
import time
import tracemalloc
import datetime
import pandas as pd


def create_medium_cases(qtd):
    medium = {}
    medium[1] = random.sample(range(qtd), qtd)
    medium[2] = random.sample(range(qtd), qtd)
    medium[3] = random.sample(range(qtd), qtd)
    medium[4] = random.sample(range(qtd), qtd)
    medium[5] = random.sample(range(qtd), qtd)
    return medium


def create_lists_insertion(qtd):
    lists = {}
    best = list(range(qtd))
    worst = list(range(qtd, 0, -1))
    lists['melhor'] = best
    lists['pior'] = worst
    lists['medio'] = create_medium_cases(qtd)
    return lists


def create_lists_merge(qtd):
    lists = {}
    par = []
    impar = []
    worst = []
    best = list(range(qtd))
    for i in range(qtd):
        if i % 2 == 0:
            par.append(i)
        else:
            impar.append(i)
    worst.append(par.reverse)
    worst.append(impar.reverse)
    lists['melhor'] = best
    lists['pior'] = worst
    lists['medio'] = create_medium_cases(qtd)
    return lists


def create_lists_quick(qtd):
    lists = {}
    best = []
    best1 = []
    best2 = []
    worst = []
    pivot = qtd % 2
    for i in range(qtd):
        best1.append(random.random(0, pivot))
        best2.append(random.random(pivot, qtd))
        worst.append(qtd - i)
    best.append(best1)
    best.append(best2)
    best.append(pivot)
    lists['melhor'] = best
    lists['pior'] = worst
    lists['medio'] = create_medium_cases(qtd)
    return lists


def measure_memory(snapshot):
    top_stats = snapshot.statistics('lineno')
    total = sum(stat.size for stat in top_stats)
    return total / 1024


def using_insertion_list(data, qtd):
    execucoes = []
    execucoes.append(execute_sort(
        data['melhor'], insertion_sort, 'insertion', qtd, 'melhor'))
    execucoes.append(execute_sort(
        data['pior'], insertion_sort, 'insertion', qtd, 'pior'))
    execucoes.append(execute_sort_caso_medio(
        data['medio'], insertion_sort, 'insertion', qtd))
    generate_csv(execucoes)
    return execucoes


def execute_sort(data, sort_algoritmo, algoritmo_nome, qtd, caso):
    linha = {}
    hora = datetime.datetime.now()
    tracemalloc.start()
    st = time.time()
    sort_algoritmo(data)
    snapshot = tracemalloc.take_snapshot()
    memory = measure_memory(snapshot)
    et = time.time()
    ut = et - st
    linha['data'] = hora
    linha['algortimo'] = algoritmo_nome
    linha['n'] = qtd
    linha['caso'] = caso
    linha['memoria/mb'] = memory
    linha['tempo/sec'] = ut
    return linha


def execute_sort_caso_medio(data, sort_algoritmo, algoritmo_nome, qtd):
    linha = {}
    hora = datetime.datetime.now()
    soma_tempo = 0
    soma_memoria = 0
    for i in data:
        tracemalloc.start()
        st = time.time()
        sort_algoritmo(data[i])
        snapshot = tracemalloc.take_snapshot()
        memory = measure_memory(snapshot)
        et = time.time()
        ut = et - st
        soma_tempo += ut
        soma_memoria += memory
        tracemalloc.stop()
    linha['data'] = hora
    linha['algortimo'] = algoritmo_nome
    linha['n'] = qtd
    linha['caso'] = 'medio'
    linha['memoria/mb'] = soma_memoria/5
    linha['tempo/sec'] = soma_tempo/5
    return linha


def using_merge_list(data, qtd):
    execucoes = []
    execucoes.append(execute_sort(
        data['melhor'], merge_sort, 'merge', qtd, 'melhor'))
    execucoes.append(execute_sort(
        data['pior'], merge_sort, 'merge', qtd, 'pior'))
    execucoes.append(execute_sort_caso_medio(
        data['medio'], merge_sort, 'merge', qtd))
    generate_csv(execucoes)


def using_quick_list(data, qtd):
    execucoes = []
    execucoes.append(execute_sort(
        data['melhor'], quick_sort, 'quick', qtd, 'melhor'))
    execucoes.append(execute_sort(
        data['pior'], quick_sort, 'quick', qtd, 'pior'))
    execucoes.append(execute_sort_caso_medio(
        data['medio'], quick_sort, 'quick', qtd))
    generate_csv(execucoes)


def generate_csv(data):
    df = pd.DataFrame.from_dict(data)
    df.to_csv('execucoes.csv')
    print("Arquivo criado: execucoes.csv")


def main():
    print("Digite a quantidade de numeros a serem ordenados")
    qtd = input()
    qtd = int(qtd)
    print("Agora digite um dos algoritmos abaixo")
    print("1 - Insertion Sort")
    print("2 - Merge Sort")
    print("3 - Quick Sort")
    algoritmo = input()
    data = {}
    if algoritmo == '1':
        print('Algortimo selecionado: Insertion Sort')
        data = create_lists_insertion(qtd)
        using_insertion_list(data, qtd)
    elif algoritmo == '2':
        print('Algortimo selecionado: Merge Sort')
        data = create_lists_merge(qtd)
        using_merge_list(data, qtd)
    else:
        print('Algortimo selecionado: Quick Sort')
        data = create_lists_quick(qtd)
        using_quick_list(data, qtd)


main()
