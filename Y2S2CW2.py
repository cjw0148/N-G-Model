import numpy as np
import matplotlib.pyplot as plt
import random
from random import randrange

def mvng_cars(state): 
	
	t = 0
	
	for i in range(len(state)):
		
		if state[i] > 0:
			
			t=t+1
	
	return t 
	

def stop_cars(state): 
	
	s = 0
	
	for i in range(len(state)):
		
		if state[i] == 0:
			
			s=s+1
	
	return s 


def car_avg_v(state,maxv,carpos,ncar):
	
	car_v = np.zeros(ncar)
	c=0
	
	for i in range(len(state)):
		
		if state[i] != -1:
			
			car_v[c] = state[i]
			c = c+1
	car_avg = np.mean(car_v)
	
	return car_avg

def apply_rule(state,maxv,carpos,n,prob):
	c = 0
	for i in range(len(state)):
		a = 0
		b = 1
		
		if state[i] >= 0: #finds the car
			
			
			for j in range(maxv):#checks postions in front of cars to determine accel and deccel
				if i + j + 1 <= n:
					t = i + j + 1
				else:
					
					t = i + j + - n
				
				if state[t] == -1 and b==1:
					
					a = a+1
					
				elif state[t] != -1:
										b = 0
			#updates speeds of cars and adds curent postion to an array for ease of calling later	
			if int(state[i]) < a:

				state[i] = state[i] + 1 
				carpos[c] = i
					
			elif state[i] > a:
				
				state[i] = a
				carpos[c] = i
			
			elif state[i] == a:
				
				carpos[c] = i
		
			c=c+1#changes array position next car position will be updated to
			
	
	nstate = np.zeros(n+1, dtype=int)#new array to have new postions and speeds
	
	for o in range(len(nstate)):#makes all nstate vals 0
		
		nstate[o] = -1
	
	#loops through pos of cars to randomly lower speeds by one down to a minimum of 0
	for m in range(len(carpos)):
		
		coin = random.randint(1,1000)
		probab = prob*1000
		if state[carpos[m]] > 0 and coin <= probab :
			
			state[carpos[m]] = state[carpos[m]] - 1
			
	
		
	
	for k in range(len(carpos)):
	
		#updates new array with 
		if carpos[k] + int(state[int(carpos[k])]) <= n:
			
			nstate[carpos[k] + state[carpos[k]]] = state[carpos[k]]	#updates new array with 
		
		elif carpos[k] + int(state[int(carpos[k])]) > n:
			
			
			nstate[int(carpos[k]) + int(state[int(carpos[k])]) - n -1 ] = int(state[int(carpos[k])])
	
	return nstate	
def evolve(istate, steps,maxv,carpos,n,prob,ncar):
	state = istate.copy()
	history = [state.copy()]
	
	caravs = np.zeros(steps)
	t = 0
	
	for k in range(steps):
		car_avg = car_avg_v(state,maxv,carpos,ncar)
		state = apply_rule(state,maxv,carpos,n,prob)
		history.append(state.copy())
		caravs[t] = car_avg
		t = t+1
	
	car_average = np.mean(caravs)
	
	return history, car_average
def plot_evolution(history):
	plt.figure(figsize=(10, 5))
	plt.imshow(history)
	plt.xlabel("Cell",fontsize=16)
	plt.ylabel("Time Step",fontsize=16)
	plt.title("Graph of cars on the road",fontsize=16)
	plt.show()

n = int(input("Enter the length of the road ")) #sets length of road

count = 0 #count for the loop to randomly place cars

ncar = int(input("Enter car number ")) #sets car number

maxv = 5#sets max speed

#creates array of 0's for the road then makes them -1 so speeds from 0 up can be stored in the same array
istate = np.zeros(n+1, dtype=int)
for i in range(len(istate)):
	istate[i] = -1

#randomly places cars in array until ncar's have been placed
while count != ncar:

	pos = random.randint(0,n)				
	speed = random.randint(1,maxv)
	
	if istate[pos] == -1:
		
		istate[pos] = speed
		count = count + 1

prob = float(input("Enter the probability of a car slowing down at random "))

carpos = np.zeros(ncar, dtype=int)#creates an array to store car positions

steps = int(input("Enter the number of time steps to run ")) #sets numbers of time intervals will be run
evolution_history,car_avg_speed = evolve(istate,steps,maxv,carpos,n,prob,ncar)#array of the state arrays of over the time intervals

plot_evolution(np.array(evolution_history))#plots array of arrays aginst time




print(car_avg_speed)


