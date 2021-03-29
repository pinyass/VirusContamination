import math
import random
import tkinter as tk

class Simulation():
    def __init__(self):
        '''initialization'''
        self.day_number = 1

        '''taking population size as input'''
        self.population_size = int(input('Enter the population size : '))
        '''checking if i/p is perfect square(for vissual purpose as in gui pannel will be NxN) and setting grid value'''
        root = math.sqrt(self.population_size)
        if int(root+0.5)**2 != self.population_size:
        	root = round(root,0)
        	self.grid_size = int(root)
        	self.population_size = self.grid_size**2
        	print('population size rounded to : {}'.format(self.population_size))
        else:
        	self.grid_size = int(math.sqrt(self.population_size))

        self.infection_percent = float(input('Enter the percentage of population infected initially : '))
        self.infection_percent /= 100

        self.infection_probability = float(input('Enter the probability that a person might get infected : '))

        self.infection_duration = int(input('Enter the duration of the infection : '))

        self.mortality_rate = float(input('Enter the mortality rate of the infection : '))

        self.sim_days = int(input('Enter number of days to simulate : '))

class Person():
    '''modelling person'''
    def __init__(self):
        '''initializing'''
        self.is_infected = False
        self.is_dead = False
        self.days_infected = 0

    def infect(self, simulation):
        '''infect a person based on infection conditions'''
        if random.randint(0,100) < simulation.infection_probability:
            self.is_infected = True
    
    def heal(self):
        '''healing a person'''
        self.is_infected = False
        self.days_infected = 0

    def die(self):
        self.is_dead = True

    def update(self, simulation):
        '''check if person is infected. if true then increase number of days infected.if dying criteria is met then , the person will die'''
        '''check if person alive'''
        if not self.is_dead:
            '''check if person infected'''
            if self.is_infected:
                self.days_infected += 1
                '''check if person will die'''
                if random.randint(0,100) < simulation.mortality_rate:
                    self.die()
                    '''heal person if infection over'''
                elif self.days_infected == simulation.infection_duration:
                    self.heal()


class Population():
    '''modelling the population'''
    def __init__(self, simulation):
        '''initialization'''
        self.population = [] # N x N lits
        #looping through needed no. of rows
        for i in range(simulation.grid_size):
            row = []
            #loop through persons in each row
            for j in range(simulation.grid_size):
                person = Person()
                row.append(person)
            self.population.append(row)


    def initial_infection(self, simulation):
        '''infect initial population based on conditions'''
        #total infected = infected_percent x population_size
        infected_count = int(round(simulation.infection_percent*simulation.population_size, 0))
        
        infections = 0

        while infections < infected_count:
            #selecting random person to infect
            x = random.randint(0, simulation.grid_size-1)
            y = random.randint(0, simulation.grid_size-1)

            if not self.population[x][y].is_infected:
                self.population[x][y].is_infected = True
                self.population[x][y].days_infected = 1
                infections += 1


    def spread_infection(self, simulation):
        #random person -> self.population[x][y]
        #person to his right -> self.population[x][y+1]
        #person to his left -> self.population[x][y-1]
        #person above him -> self.population[x-1][y]
        #person below him -> self.population[x+1][y]
        
        #loop through population
        for i in range(simulation.grid_size):
            #loop through people in row
            for j in range(simulation.grid_size):
                #check if person is dead
                if self.population[i][j].is_dead == False:
                    #check to see if he'll be infected
                    #if i=0 and j=0 ,we're in 1st row 1st column
                    if i == 0:
                        if j == 0:
                            #in first column, we can't look left
                            if self.population[i][j+1].is_infected or self.population[i+1][j].is_infected:
                                self.population[i][j].infect(simulation)
                                #in last column , we cn't look right
                        elif j == simulation.grid_size-1:
                            if self.population[i][j-1].is_infected or self.population[i+1][j].is_infected:
                                self.population[i][j].infect(simulation)
                        #in any other column, we can look left right or below
                        else:
                            if self.population[i][j-1].is_infected or self.population[i][j+1].is_infected or self.population[i+1][j]:
                                self.population[i][j].infect(simulation)
                    #if i=simulation.grid_size-1, we're i nlast column and if j=simulation.grid_size-1,we're in last row
                    elif i == simulation.grid_size-1:
                        if j == 0:
                            if self.population[i][j-1].is_infected or self.population[i-1][j].is_infected:
                                self.population[i][j].infect(simulation)
                        elif j == simulation.grid_size-1:
                            if self.population[i][j-1].is_infected or self.population[i-1][j].is_infected:
                                self.population[i][j].infect(simulation)
                        else:
                            if self.population[i][j-1].is_infected or self.population[i][j+1].is_infected or self.population[i-1][j].is_infected:
                                self.population[i][j].infect(simulation)                   
                #any row for i != 0 or j != 0
                    else:
                        if j == 0:
                            if self.population[i][j+1].is_infected or self.population[i+1][j].is_infected or self.population[i-1][j].is_infected:
                                self.population[i][j].infect(simulation)
                        elif j == simulation.grid_size-1:
                            if self.population[i][j-1].is_infected or self.population[i+1][j].is_infected or self.population[i-1][j].is_infected:
                                    self.population[i][j].infect(simulation)
                        else:
                            if self.population[i][j-1].is_infected or self.population[i][j+1].is_infected or self.population[i+1][j] or self.population[i-1][j].is_infected:
                                    self.population[i][j].infect(simulation)


    def update(self, simulation):
        '''updating status'''
        simulation.day_number += 1
        for row in self.population:
            for person in row:
                person.update(simulation)


    def display_statistics(self, simulation):
        '''display stats'''
        total_infected_count = 0
        total_death_count = 0
        #looping through each row in the population grid
        for row in self.population:
            #looping through eavh person in the row
            #person infected
            for person in row:
                if person.is_infected:
                    total_infected_count += 1
                    #person dead
                    if person.is_dead:
                        total_death_count += 1
        
        #calculating percentage o fpopulation that is infected and dead
        infected_percent = round(100*(total_infected_count/simulation.population_size), 4)
        death_percent = round(100*(total_death_count/simulation.population_size), 4)

        #stats summary
        print('\n----DAY : ' + str(simulation.day_number))
        print('Infected percent : ' + str(infected_percent) + '%')
        print('Dead percent : ' + str(death_percent) + '%')
        print('Total infected : ' + str(total_infected_count) + ' / ' + str(simulation.population_size))
        print('Total dead : ' + str(total_death_count) + ' / ' + str(simulation.population_size))


def graphics(simulation, population, canvas):
    square_dimension = 600//simulation.grid_size
    for i in range(simulation.grid_size):
        y= i*square_dimension
        for j in range(simulation.grid_size):
            x = j*square_dimension

            #check if person is dead
            if population.population[i][j].is_dead:
                canvas.create_rectangle(x, y, x+square_dimension, y+square_dimension, fill='red')
            else:
                if population.population[i][j].is_infected:
                    canvas.create_rectangle(x, y, x+square_dimension, y+square_dimension, fill='yellow')
                else:
                    canvas.create_rectangle(x, y, x+square_dimension, y+square_dimension, fill='green')


sim = Simulation()
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600

sim_window = tk.Tk()
sim_window.title('Epedemic outbrake')
sim_canvas = tk.Canvas(sim_window, width= WINDOW_WIDTH, height= WINDOW_HEIGHT, bg='lightblue')
sim_canvas.pack(side=tk.LEFT)

pop = Population(sim)

pop.initial_infection(sim)
pop.display_statistics(sim)
input('Press ENTER')

for i in range(1, sim.sim_days):

    pop.spread_infection(sim)
    pop.update(sim)
    pop.display_statistics(sim)
    graphics(sim, pop, sim_canvas)

    sim_window.update()

    if i != sim.sim_days-1:
        sim_canvas.delete('all')
