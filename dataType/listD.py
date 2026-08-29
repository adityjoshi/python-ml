lists = [1,2,3,4,5]

# index
print(lists[1])
print(lists[-1])

# slicing
print(lists[0:2])
print(lists[:3])
print(lists[3:])
print(lists[::2])
print(lists[::-1])


#append
lists.append(6)
print(lists)

#extend
lists.extend([7,8,9])
print(lists)

#insert
lists.insert(1,100)
print(lists)

# remove(10), lists.pop() removes and returns pop(1) removes by index
# lists.clear() clears the lists
# .index(5) returns the index of the element

# count
print(lists.count(1))

#sort vs sorted
lists.sort()
s = sorted(lists)
print(lists,s)

#reverse() vs reversed(lists)

# LOOPS
for i in lists:
    print(i,end=" ")

print()
for i in range(len(lists)):
    print(lists[i], end=" ")

print()

# enumerate better way to get index as well as element
for i,name in enumerate(lists):
    print(f"{i}:{name}",end=" ")
print()

for i,name in enumerate(lists,start=1):
    print(f"{i}:{name}",end=" ")
print()


# Input

#  x = input()
# print(x.split())

#x = list(map(int, input().split()))
#print(x)

#split with different delimeter
#y = list(map(str,input().split(",")))
#print(y)

#join
words = ["hello", "world"]
print(" ".join(words))
