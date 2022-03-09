import pprint
pp = pprint.PrettyPrinter(indent=4)

k = 2


# function for the creation of K-dimentional tree 
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


#Point insertion Function
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


#Searching for a specific point in the Tree
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

#Delete a point from the tree
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

points =  [(30,40), (5,25), (10,12), (70,70), (50,30), (35,45)]
print('Initial points to store in KD - TREE: ', points)
print('KD TREE: ')
KD = build_kdtree(points)
pp.pprint(KD)

print()
print()

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
