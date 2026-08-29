t = (10,20,20,30)
print(t[::-1])

#single element tuple
single_element = (10,)

#tuple count and index
print(t.count(20))
print(t.index(20))


# Set
a = {1,2,3,5}
b = {2,4,5,6}
print(a.union(b)) # |
print(a.difference(b)) # -
print(a.intersection(b)) # &

a.add(9)
a.remove(3)
print(a)
