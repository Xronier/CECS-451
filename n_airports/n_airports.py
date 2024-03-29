# -*- coding: utf-8 -*-
"""n-airports my var.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jiwchjwz7k4qteaSv9xNrnJ6fauA6I4l
"""

import random
import numpy as np
import math
import matplotlib.pyplot as plt
 
 
def get_closest_air(cities, airports):
  cities = list(cities)
  # List that holds a list for all airports that contain the cities with the closest
  # distance to them.
  closest_air = [[] for x in range(len(airports))]
 
  for c in range(len(cities)):
    # Record the distance from c to all airports
    city_to_air = []
 
    for i in range(len(airports)):
      # Calculate the distance from the current city to the current airport
      distance = math.hypot(airports[i][0] - cities[c][0], airports[i][1] - cities[c][1])
      city_to_air.append(distance)
 
    # Find the closest airport to the current city and append it to its respective
    # list.
    air_dist = min(city_to_air)
    air_num = city_to_air.index(air_dist)
    closest_air[air_num].append(cities[c]) # ?
 
  return closest_air
 
# Get the objective function of the current airports
def get_obj_func(airports, min_distances):
  obj_func = 0
  for i in range(len(airports)):
    for c in range(len(min_distances[i])):
      obj_func += math.hypot(airports[i][0] - min_distances[i][c][0], airports[i][1] - min_distances[i][c][1])
  
  return obj_func
 
# Generate new airports based on the current one's locations and the cities closest to it
def get_gradient(airports, min_distances, alpha):
  delta_f = []
  # Get partial derivatives of f
  for i in range(len(airports)):
    partial_x = 0
    partial_y = 0
    for c in range(len(min_distances[i])):
      partial_x += airports[i][0] - min_distances[i][c][0]
      partial_y += airports[i][1] - min_distances[i][c][1]
    delta_f.append((partial_x * 2, partial_y * 2))
 
  # Apply the gradient to delta_f, creating new airport locations
  gradient = []
  for i in range(len(delta_f)):
    gradient.append((airports[i][0] - alpha * delta_f[i][0], airports[i][1] - alpha * delta_f[i][1]))
  print("Gradient", gradient)
  return gradient
     
def graph(cities, airports):
  zip_cities = zip(*cities)
  plt.scatter(*zip_cities, marker='+',color='b', label='Cities')
  zip_airs = zip(*airports)
  plt.scatter(*zip_airs, marker='*', color='r', s=100, label='Airports')
  plt.legend()
  plt.show()
 
def main():
  num_city = 100
  num_air = 3
  num_center = 5
  sigma = 0.1
  cities = set()
  airports = []
  alpha = .01
  # ------------------- initial airport locations --------------------------
  for i in range(num_center):
      x = random.random()
      y = random.random()
      xc = np.random.normal(x, sigma, num_city//num_center)
      yc = np.random.normal(y, sigma, num_city//num_center)
      cities = cities.union(zip(xc, yc))
 
  for i in range(num_air):
      x = random.random()
      y = random.random()
      airports.append((x,y)) 
 
  zip_cities = zip(*cities)
  plt.scatter(*zip_cities, marker='+',color='b', label='Cities')
  zip_airs = zip(*airports)
  plt.scatter(*zip_airs, marker='*', color='r', s=100, label='Airports')
  plt.legend()
  plt
  # ------------------------------------------------------------------------
 
  # Generate new airports off the initial locations
  min_distances = get_closest_air(cities, airports)
  new_airports = get_gradient(airports, min_distances, alpha)
  graph(cities, new_airports)
  obj_func = get_obj_func(airports, min_distances)
 
  converging = False
  benchmark = .00005
  # Until the objective function < .005 continue generating new airport locations
  while not converging:
    # Generate news airport off the previous locations
    print("Old Airports", new_airports)
    min_distances = get_closest_air(cities, new_airports)
    new_airports = get_gradient(new_airports, min_distances, alpha)
    print("New Airports", new_airports)
 
    # Check if the objective function is < .005
    temp_obj_func = get_obj_func(new_airports, min_distances)
 
    if (obj_func - temp_obj_func > benchmark): # If it isn't, continue looping
      obj_func = temp_obj_func
    else: # If it is, the cities are in an efficient location so break out of the loop
      print("Converged")
      converging = True
      
    print("Objective Function", obj_func)
    graph(cities, new_airports)
 
main()