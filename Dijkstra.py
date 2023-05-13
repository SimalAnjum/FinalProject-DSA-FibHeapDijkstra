from FibonacciHeap import Heap
import math


def dijkstra(adjList, source, sink = None):
    n = len(adjList)
    visited = [False]*n
    distance = [float("inf")]*n

    heapNodes = [None]*n
    heap = Heap()
    for i in range(1, n):
        heapNodes[i] = heap.Insert(float("inf"), i)  # distance, label

    distance[source] = 0
    heap.DecreaseKey(heapNodes[source], 0)

    while heap.total_nodes:
        current = heap.ExtractMin().value
        visited[current] = True

        if sink and current == sink:
            break

        for (neighbor, weight) in adjList[current]:
            if not visited[neighbor]:
                if distance[current] + weight < distance[neighbor]:
                    distance[neighbor] = distance[current] + weight
                    heap.DecreaseKey(heapNodes[neighbor], distance[neighbor])

    return distance

with open('Adjacency Lists.txt') as f:
    lines = f.readlines()

for x in lines:
    adjList = eval(x)
    print(x)
    print('enter source node')
    src = int(input())
    print(dijkstra(adjList, src, None))