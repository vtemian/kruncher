import random


NAMES = ['Vlad', 'Bogdan', 'Andrei', 'Cristi']

with open('data.txt', 'w') as f:
  head = 'Name,Income1,Income2,Spending1,Spending2'
  f.write(head + '\n')
  k = 0
  while k < 999:
    name = NAMES[random.randint(0, 3)]
    value = ','.join(str(random.randint(0, 999)) for x in range(4))
    value = "%s,%s\n" % (name, value)
    f.write(value)
    k += 1
