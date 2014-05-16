# ----------------------------------- Selection of Survivors
def survivors_generational(parents,offspring):
    return offspring

def survivors_steady_state(parents,offspring):
    """Minimizing."""
    size = len(parents)
    parents.extend(offspring)
    parents.sort(key=itemgetter(1))
    return parents[:size]

def best_pop(population):
    """minimization"""
    population.sort(key=itemgetter(1))
    return population[0]
