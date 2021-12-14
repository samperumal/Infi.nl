from functools import reduce

with open("input.txt", "r") as f:
  # Parse input
  miss_count = int(f.readline().strip().split(" ")[0])
  nodelist = [[n for n in line.strip().split(":")] for line in f.readlines()]
  nodes = {}
  for n in nodelist:
    nodes[n[0]] = [(y[1], int(y[0])) for y in [x.split(" ") for x in n[1].strip().split(", ")] ]

  # Check input parsed correctly
  for n in nodes:
    print(n, nodes[n])

  print()

  # Identify ingredients
  onderdelen = set(map(lambda a: a[0], reduce(lambda a, b: a + b, nodes.values())))

  print(onderdelen)  
  print()
  
  # Perform tail recursion to calculate quantity of base ingredients
  # required per onderdeel, flattening the virtual onderdelen graph
  flat_nodes = {}

  for output in nodes:
    inputs = [n for n in nodes[output]]
    deep_inputs = []
    while len(inputs) > 0:
      ingredient, quantity = inputs.pop()
      if ingredient in nodes:
        for sub_ingredient, sub_quantity in nodes[ingredient]:
          inputs.append((sub_ingredient, quantity * sub_quantity))
        pass
      else:
        deep_inputs.append((ingredient, quantity))
    flat_nodes[output] = deep_inputs

  # Find speelgoed (items not used as an ingredient anywhere)
  # and the total base ingredients required for 1 unit

  valid_speelgoed = []

  for n in flat_nodes:
    if not n in onderdelen:
      speelgoed = (n, sum(map(lambda a: a[1], flat_nodes[n])))
      valid_speelgoed.append(speelgoed)

  valid_speelgoed.sort(key = lambda a: a[1], reverse=True)
  print(valid_speelgoed)
  print()

  # Attempt packing solutions until the correct one is found
  # 
  # Recursively add the speelgoed met de grootste aantal onderdelen
  # while the total onderdelen and speelgooed aantal are less than the 
  # target, then move on to the next biggest
  end_index = len(valid_speelgoed)

  def pack(index, stack, total):
    if total == miss_count and len(stack) == 20:
      # print(stack)
      return True

    while index < end_index:
      if total + valid_speelgoed[index][1] <= miss_count:
        stack.append(valid_speelgoed[index])
        if pack(index, stack, total + valid_speelgoed[index][1]):
          return True
        stack.pop()
      index += 1
    
    return False

  stack = []
  pack(0, stack, 0)
  
  # print(stack)
  # print()

  # Print output
  print("Aantal missende onderdelen:", sum(map(lambda a: a[1], stack)))
  print()
  print("Grootste aantal onderdelen:", max(map(lambda a: a[1], valid_speelgoed)))
  print("Speelgoedlijst            :", "".join(sorted(map(lambda a: a[0][0], stack))))