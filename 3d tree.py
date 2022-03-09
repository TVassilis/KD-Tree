import pprint
import time
import tracemalloc
pp = pprint.PrettyPrinter(indent=4)

k = 3

def build_kdtree(points, depth=0):
    n = len(points)

    if n <= 0:
        return None

    axis = depth % k

    sorted_points = sorted(points, key=lambda point: point[axis])

    return {
        'point': sorted_points[n // 2],
        'left': build_kdtree(sorted_points[:n // 2], depth + 1),
        'right': build_kdtree(sorted_points[n // 2 + 1:], depth + 1)
    }

def insert(point, tree, depth=0):
  
  axis = depth % k

  if tree == None:
    tree = {
      'point': point,
      'left': None,
      'right': None,
    }

  else:
    
    if point[axis] <= tree['point'][axis]:
      tree['left'] = insert(point, tree['left'] ,depth + 1)

    else:
      tree['right'] = insert(point, tree['right'], depth + 1)

  return tree

def search(point, tree, depth=0):

  axis = depth % k
  
  if tree == None:
    return False 

  else:
    if point == tree['point']:
      return True 

    elif point[axis] <= tree['point'][axis]:
      return search(point, tree['left'], depth + 1)

    elif point[axis] > tree['point'][axis]:
      return search(point, tree['right'] ,depth + 1)


def find_min(tree, dim, depth=0):

  if tree is None:
    return None
  
  axis = depth % k
  
  
  if axis == dim:
    if tree['left'] is None:
      return tree['point']
    else:
      return find_min(tree['left'], dim, depth + 1)
  else:
    #return min(tree['point'],  find_min(tree['left'], dim, depth + 1), find_min(tree['right'], dim, depth + 1))
    min_node = None
    min_left = find_min(tree['left'], dim, depth + 1)
    min_right = find_min(tree['right'], dim, depth + 1)

    if min_left and min_right:
      if min_left[dim] < min_right[dim]:
        min_node = min_left
      else:
        min_node = min_right

    else:
      min_node = min_left or min_right

    if min_node:
      if tree['point'][dim] < min_node[dim]:
        min_node = tree['point']
      return  min_node
    else:
      return tree['point']

def delete(point, tree, depth=0):

  if tree is None:
    return None

  axis = depth % k

  if point == tree['point']:
    if tree['right']:
      tree['point'] = find_min(tree['right'], axis, depth + 1)
      tree['right'] = delete(tree['point'], tree['right'], depth + 1)

    elif tree['left']:
      tree['point'] = find_min(tree['left'], axis, depth + 1)
      tree['right'] = delete(tree['point'], tree['right'], depth + 1)
      tree['left'] = None

    else:
      tree = None

  elif point[axis] < tree['point'][axis]:
    tree['left'] = delete(point, tree['left'], depth + 1)

  else:
    tree['right'] = delete(point, tree['right'], depth + 1)

  return tree



# --- DEMONSTRATION CODE FOR KD TREE (2-DIMENSIONAL) ---  

points = []
file = open("data3.txt", "r")
for line in file:
    points.append(eval(line))
file.close()


print('KD TREE: ')
start_time = time.time()
tracemalloc.start()
KD = build_kdtree(points)
elapsed_time = time.time() - start_time
print("3D Tree build: ", elapsed_time)
current, peak = tracemalloc.get_traced_memory()
print("Current memory usage is {"+str(current / 10**6)+"}MB Peak was {"+str(peak / 10**6)+"}MB")
tracemalloc.stop()
print()
print()

start_time = time.time()
for point in points:
  searchNode = search(point, KD, 0)
elapsed_time = time.time() - start_time
print("3D Tree Search: ", elapsed_time)

print()
print()

start_time = time.time()
print("Searhing point (57012, 37189, 10595)")
searchNode = search((57012, 37189, 10595), KD, 0)
print(searchNode)
elapsed_time = time.time() - start_time
print("3D Tree Search: ", elapsed_time)

print()
start_time = time.time()
print("Inserting point (65004, 87369,11256)")
insertNode = insert((65004, 87369,11256), KD, 0)
elapsed_time = time.time() - start_time
print("3D insert: ", elapsed_time)
print("Searching point: (65004, 87369,11256)")
print(search((65004, 87369,11256), KD, 0))

print()
start_time = time.time()
print("Deleting point (65004, 87369,11256)")
delete((65004, 87369,11256), KD, 0)
elapsed_time = time.time() - start_time
print("3D delete node: ", elapsed_time)
print("Searching point: (65004, 87369,11256)")
print(search((65004, 87369,11256), KD, 0))


'''
print('INSERTING POINT (25,25): ')
point1 = (25,25)
insert(point1, KD, 0)
pp.pprint(KD)

print()
print()
print('SEARCHING POINT (25,25): ')
print(search((25,25), KD, 0))
print('SEARCHING POINT (25,24): ')
print(search((25,24), KD, 0))

print()
print()
print('INSERTING MINIMUM X-axis POINT: (1,3).')
point2 = (1,3)
insert(point2, KD, 0)
pp.pprint(KD)

print()
print()
print('INSERTING MINIMUM Y-axis POINT: (3,2)')
point3 = (3,2)
insert(point3, KD, 0)
pp.pprint(KD)

print()
print()
print('FIND THE MINIMUM OF X-axis')
print(find_min(KD, 0, 0))
print('FIND THE MINIMUM OF Y-axis')
print(find_min(KD, 1, 0))
#pp.pprint(KD)

print()
print()
print('INSERTING POINT (12,18): ')
point4 = (12,18)
insert(point4, KD, 0)
pp.pprint(KD)

print()
print()
print('THE KD TREE AFTER DELETING POINT (10,12):')
delete((10,12), KD, 0)
pp.pprint(KD)
#print(search((1,3), KD, 0))
'''