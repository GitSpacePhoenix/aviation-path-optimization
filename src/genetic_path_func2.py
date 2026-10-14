import numpy as np
import matplotlib.pyplot as plt
import random as rd


def genetic_path_f(START_POINT, END_POINT, STORM):

		# 1. create_indivdual() : Generates a random fligth path (chromosome)
	# 2. create_population(size) : Creates a list of individuals
	# 3. callculate_fitness(individual) : Caculates the cost of a route. Lower is better
	
	def create_individual():
	    # Ceate a random x and y coordinates between start and end
	    x_coords = np.linspace(START_POINT[0], END_POINT[0], NUM_WAYPOINTS + 2)
	    # Add a random noise to y coordinates, except start and end
	    y_coords = np.linspace(START_POINT[1], END_POINT[1], NUM_WAYPOINTS + 2)
	    y_coords[1:-1] = np.random.uniform(-30, 30, NUM_WAYPOINTS)
	
	    #Finally we return coordiantes as an array [x,y]
	    return np.column_stack((x_coords, y_coords))
	
	
	def create_population(size):
	    return [create_individual() for _ in range(size)]
	
	"""
	def calculate_fitness(individual):
	
	    distance = 0
	    penality = 0
	
	    for i in range(1, len(individual)):
	        p1 = individual[i-1]
	        p2 = individual[i]
	
	        # calculate the Euclidean distance between two consecutive points within the ‘individual’ list
	
	        dist = np.linalg.norm(p2 - p1)
	        distance += dist
	
	        # Chcck storm penality for the waypoint
	        dist_to_storm = np.linalg.norm(p2 - np.array([STORM[0], STORM[1]]))
	        if dist_to_storm < STORM[2]:
	            penality += 1000 # High penality for fliying into the storm
	
	    # We invert the cost so higer fitness = better route


	    total_cost = distance + penality
	    return 1.0 / total_cost
	
	"""
	# NEW FITNESS VERSION (uses vectors)
	
	import matplotlib.pyplot as pĺt
	# NEW FINTESS VERSION (uses vectors)
	def calculate_fitness(individual, STORM):
	    distance = 0
	    penality = 0
	
	    # Extract storm coordinates as follows:
	    C = np.array([STORM[0], STORM[1]])
	    R = STORM[2]
	
	    #Array to store length of each segment for variance calculation
	    segment_lengths = []
	
	    for i in range(1, len(individual)):
	        A = individual[i-1] #initial position
	        B = individual[i] #final position
	
	        # calculate the Euclidean distance between two consecutive points within the ‘individual’ list
	        dist = np.linalg.norm(B-A)
	        distance += dist
	        # Store the length for penality
	        segment_lengths.append(dist)
	
	        # Math formulas to avoid storms
	        AB = B - A
	        AC = C - A
	
	        # Dot product
	        dot_product = np.dot(AC, AB)
	        # The squareof the length of AB (AB at point AB)
	        ab_squared = np.dot(AB, AB)
	
	        # Avoid division by zero if A and B are the same point (rare bus posible in extreme mutations)
	
	        if ab_squared == 0:
	            closest_point = A
	        else:
	            # here we calculate t and clip it between 0 and 1
	            t = max(0, min(1,dot_product/ab_squared))
	            # We find the exact coordinate to the nearest point
	            closest_point = A + t* AB #clossest point 'P'
	
	        # Distace from the segment to the storm
	        dist_to_storm = np.linalg.norm(closest_point - C)
	
	
	        # If the distance is less than the raduis, the line segment will intersect the storm
	        if dist_to_storm < R:
	
	            penality += 1000 + (R - dist_to_storm ) * 100
	
	    # Then calculate the variance of the length
	    length_variance = np.var(segment_lengths)
	    dispersion_penality = length_variance * 0.3
	
	    # Extended cost function
	    total_cost = distance + penality + dispersion_penality
	    return 1.0 / total_cost
	        # Pelality proportional to how far in it went ( to help the algorithm "get out")
	
	
	
	#  ----  PLOT FUNCTIONS  ----
	def plot_route(best_route, generation, cost):
	
	
	    plt.figure(figsize=(8,8))
	
	    #Extract X and Y from the route
	    x_coords = best_route[:, 0]
	    y_coords = best_route[:, 1]
	
	
	    #Route drawing
	    plt.plot(x_coords, y_coords, marker='o', color='blue',
	             label='Fliying path', linewidth = 2)
	    plt.scatter(START_POINT[0], START_POINT[1], color='green', s=100,
	                label='Origin', zorder=5)
	    plt.scatter(END_POINT[0], END_POINT[1], color='purple', s=100,
	                label='Destiny', zorder=5)
	
	
	    #Storm drawing
	    storm_circle = plt.Circle((STORM[0], STORM[1]), STORM[2], color = 'red',
	                              alpha = 0.3, label = 'Storm dangerous zone')
	
	    plt.gca().add_patch(storm_circle)
	
	    # Define plot limits
	
	    plt.xlim(-10, 110)
	    plt.ylim(-10, 110)
	    plt.grid(True, linestyle = '--', alpha = 0.6)
	    plt.title(f'Generation : {generation} | Route cost : {cost:.2f}')
	    plt.legend()
	    plt.xlabel('X coordinate (km)')
	    plt.ylabel('Y coordinate (km)')
	
	    plt.show()
	
	
	
	def selection(population, fitness_scores):
	    # Here starts the tournament selection to find a parent
	    # Select random indices for the tournament
	    selected_indices = rd.sample(range(len(population)), TOURNAMENT_SIZE)
	
	
	    # Find the index of the best individual in the tournament
	    best_idx = selected_indices[0]
	    best_fitness = fitness_scores[best_idx]
	
	    # Replace best fitness if fitness_scores > best_fitness
	    for idx in selected_indices[1:]:
	        if fitness_scores[idx] > best_fitness:
	            best_idx = idx
	            best_fitness = fitness_scores[idx]
	
	    return population[best_idx]
	
	# Define crossover eq using the previous eq gived
	
	def crossover(first_parent, second_parent):
	    # The variable inherits the dimensions of the parent
	    child = np.zeros_like(first_parent)
	    # Start and end points remain fixed
	    # from previuos lines we remember that
	    # START_POINT = np.array([0, 0])
	    # END_POINT = np.array([100, 100])
	    child[0] = START_POINT
	    child[-1] = END_POINT
	
	    for i in range(1, len(first_parent) - 1):
	        alpha = rd.random()
	        child[i] = alpha*first_parent[i] + (1 - alpha)*second_parent[i]
	    return child
	
	
	# Define mutant function from a gaussian distribution
	
	def mutate(individual):
	    # We dont mutate start[0] or end [-1] ponts
	    for i in range(1, len(individual) - 1):
	        # The mutation rate is the probability that an
	        # individual will undergo a mutation
	        if rd.random() < MUTATION_RATE:
	            # Apply gaussian noise to x and y
	            individual[i][0] += rd.gauss(0, MUTATION_STDEV)
	            individual[i][1] += rd.gauss(0, MUTATION_STDEV)
	    return individual
	
	
	# --- SIMUÑATION PARAMETERS
	POPULATION_SIZE = 50
	NUM_WAYPOINTS = 6 # Points bwtween start and end

	# --- Test the intial set up
	population = create_population(POPULATION_SIZE)
	fitness_scores = [calculate_fitness(ind, STORM) for ind in population]
	
	# Get the best one from this random generation
	best_initial_idx = np.argmax(fitness_scores)
	best_initial_route = population[best_initial_idx]
	
	print(f"Best initial cost (inverted fitness): {1.0 / fitness_scores[best_initial_idx]:.2f}")
	
	
	#Here we use the population from the previuos step
	current_population = population
	
	# --- . Evolution parametrs ---
	TOURNAMENT_SIZE = 5
	MUTATION_RATE = 0.16
	# Standard deviation for gaussian noise (sigmas)
	MUTATION_STDEV = 5
	GENERATIONS = 100
	
	for gen in range(GENERATIONS):
	    # First we calculate all fitness scores from our current population
	    fitness_scores = [calculate_fitness(ind, STORM) for ind in current_population]
	    next_generation = []
	
	    # Elitism:keep the absolute best indivudual untouched
	    best_idx = np.argmax(fitness_scores) # get max fitness score index
	    # Append the best current individual
	    next_generation.append(current_population[best_idx])
	
	    # Breed the rest of the new generation
	    while len(next_generation) < POPULATION_SIZE:
	        # First selection
	        first_parent = selection(current_population, fitness_scores)
	        # Second selection
	        second_parent = selection(current_population, fitness_scores)
	
	        child = crossover(first_parent, second_parent)
	        child = mutate(child)
	
	        next_generation.append(child)
	
	    # Update the current population to the next generation
	    current_population = next_generation
	
	
    #final_fitness = [calculate_fitness(ind) for ind in current_population]  #previus
	final_fitness = [calculate_fitness(ind, STORM) for ind in current_population]
	best_final_idx = np.argmax(final_fitness)
	best_final_route = current_population[best_final_idx]
	final_best_cost = 1.0 / final_fitness[best_final_idx]
	
    #print(f"Optimized cost: {final_best_cost:.2f}")
	#retuen best_final_route, final_best_cost, GENERATIONS  #previus 
	return best_final_route, final_best_cost, GENERATIONS  #<----  Return to main