
words = open('alice.txt').read().lower().split()

# Get the set of unique words.
uniques = []
for word in words:
  if word not in uniques:
    uniques.append(word)

# Make a list of (count, unique) tuples.
counts = []
for unique in uniques:
  count = 0              # Initialize the count to zero.
  for word in words:     # Iterate over the words.
    if word == unique:   # Is this word equal to the current unique?
      count += 1         # If so, increment the count
  counts.append((count, unique))

counts.sort()            # Sorting the list puts the lowest counts first.
counts.reverse()         # Reverse it, putting the highest counts first.
# Print the ten words with the highest counts.
for i in range(min(10, len(counts))):
  count, word = counts[i]
  print('%s %' % (word, count))