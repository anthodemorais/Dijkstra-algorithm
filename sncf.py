import collections
import operator

tree = {
    "Paris Lyon": {
        "Paris Montparnasse": 15,
        "Paris Nord": 15,
        "Lyon": 75,
        "Montpellier": 125
    },
    "Paris Montparnasse": {
        "Paris Lyon": 15,
        "Bordeaux": 180,
        "Rennes": 125,
        "Paris Nord": 15
    },
    "Paris Nord": {
        "Londres": 150,
        "Paris Lyon": 15,
        "Paris Montparnasse": 15
    },
    "Londres": {
        "Paris Nord": 150
    },
    "Rennes": {
        "Paris Montparnasse": 125,
        "Brest": 75
    },
    "Bordeaux": {
        "Paris Montparnasse": 180,
        "Toulouse": 180
    },
    "Lyon": {
        "Paris Lyon": 75,
        "Marseille": 90
    },
    "Toulouse": {
        "Bordeaux": 180,
        "Montpellier": 240
    },
    "Montpellier": {
        "Toulouse": 240,
        "Paris Lyon": 125
    },
    "Marseille": {
        "Lyon": 90
    },
    "Brest": {
        "Rennes": 75
    },
    "Berlin": {
        "Munich": 120
    },
    "Munich": {
        "Berlin": 120
    }
}

def getStations(tree):
    return list(tree.keys())

def getNeighbours(tree, city):
    neighbours = []
    sorted_cities = collections.OrderedDict(tree[city])
    return list(sorted_cities.keys())

def getAllPaths(tree, city):
    cities = []
    for city in tree[city]:
        cities.append(getChildrenPath(tree, city, cities))
    return cities

def getChildrenPath(tree, city, cities):
    visited = cities
    paths = getNeighbours(tree, city)
    for path in paths:
        if path not in visited:
            visited.append(path)
            getChildrenPath(tree, path, visited)
    return visited

def isReachable(tree, city, target):
    paths = getChildrenPath(tree, city, [])
    return target in paths

# Dijkstra algorithm

# algorithme de Dijkstra : entrées - Graphe, Start, End

# INIT :

# Vérifier que End est reachable depuis Start (sinon erreur)
# Marquer toutes les destinations possibles comme étant à une distance INFINIE (INF)
# Marquer toutes les destinations possibles comme n'ayant pas de prédéacesseur 3bis. Marquer le Start comme étant à une distance 0 !
# PARCOURS DU GRAPHE Pour toutes les destinations possibles : on prend la plus proche : U

# Si U est la destination : on a trouvé !
# Si U n'est pas la destination : On récupère tous ses voisins, et on mets à jour l'annuaire des distance pour les voisins V. Si on met à jour l'annuaire avec une valeur plus petite (distance Start -> V), on remplace, le prédécesseur de V par U. On retire U des destinations possibles et on continue le parcours.
# QUAND ON A TROUVÉ LA DESTINATIONS

# En partant de la destination, on remonte les prédécesseurs.
# => On obtient alors le trajet le plus cours.

def getTrip(graph, start, end):
    if isReachable(graph, start, end):
        destinations = getChildrenPath(graph, start, [])
        times = {}
        predecessors = {}
        visited = []
        for destination in destinations:
            times[destination] = 999999
            predecessors[destination] = None
        times[start] = 0
        nearestCity = visitNearestCity(graph, times, visited)
        while nearestCity != end:
            times, predecessors, visited = tripToChildren(graph, nearestCity, end, times, predecessors, visited)
            nearestCity = visitNearestCity(graph, times, visited)
        predecessor = end
        trip = []
        print(predecessors)
        while predecessor != start:
            trip.append(predecessor)
            predecessor = predecessors[predecessor]
        trip.reverse()
        return "Path: " + str(trip) + " in: " + str(times[end]) + " minutes."
    else:
        return "Unreachable"

def tripToChildren(graph, city, end, times, predecessors, visited):
    children = sorted(graph[city].items(), key=lambda kv: kv[1])
    for child in children:
        key, value = child
        if graph[city][key] + times[city] < times[key]:
            predecessors[key] = city
            times[key] = graph[city][key] + times[city]
    visited.append(city)
    return times, predecessors, visited

def visitNearestCity(graph, times, visited):
    children = sorted(times.items(), key=lambda kv: kv[1])
    nearestCity = ""
    counter = 0
    for city, time in children:
        if city not in visited:
            nearestCity = children[counter][0]
            break
        counter += 1
    return nearestCity
    



print(getStations(tree))
print(getNeighbours(tree, "Paris Lyon"))
print(getChildrenPath(tree, "Paris Lyon", []))
print(isReachable(tree, "Paris Lyon", "Marseille"))
print(getTrip(tree, "Brest", "Marseille"))