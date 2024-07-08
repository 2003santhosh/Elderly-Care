import random
import json

with open('doctor_schedules.json', 'r') as file:
    doctor_schedules = json.load(file)

num_appointments = 3 
population_size = 50 
num_generations = 100 
mutation_rate = 0.1

def generate_random_schedule(doctor_schedules):
    schedule = {}
    doctor = random.choice(doctor_schedules)
    for day, slots in doctor['schedule'].items():
        schedule[day] = random.sample(slots, num_appointments)
    return schedule

def calculate_fitness(schedule):
    return sum(len(set(appointments)) for appointments in schedule.values())

def generate_schedule_for_customer(customer_id):
    # Initialize the population
    population = [generate_random_schedule(doctor_schedules) for _ in range(population_size)]

    for generation in range(num_generations):
        fitness_scores = [calculate_fitness(schedule) for schedule in population]

        num_parents = int(0.2 * population_size)
        parents = [population[i] for i in sorted(range(len(fitness_scores)), key=lambda i: fitness_scores[i])[:num_parents]]

        offspring = []
        while len(offspring) < population_size:
            parent1, parent2 = random.sample(parents, 2)
            crossover_point = random.choice(list(doctor_schedules[0]['schedule'].keys()))
            child = {}
            for day in doctor_schedules[0]['schedule']:
                if day == crossover_point:
                    child[day] = parent1[day]
                else:
                    child[day] = parent2[day]
            if random.random() < mutation_rate:
                day_to_mutate = random.choice(list(doctor_schedules[0]['schedule'].keys()))
                child[day_to_mutate] = random.sample(doctor_schedules[0]['schedule'][day_to_mutate], num_appointments)
            offspring.append(child)

        population = parents + offspring

    best_schedule = min(population, key=calculate_fitness)
    print(f'Schedule for Customer {customer_id}:')
    for day, appointments in best_schedule.items():
        print(f'Day: {day}, Appointments: {appointments}')

# Example: Generate schedules for multiple customers
for customer_id in range(1, 6):
    generate_schedule_for_customer(customer_id)