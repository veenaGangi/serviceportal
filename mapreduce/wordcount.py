#!/usr/local/bin/python3.8

from mapreduce import MapReduce

class WordCount(MapReduce):

    def mapper(self, _, line):
        for word in line.split(" "):
            yield (word.strip(),1)

    def combiner(self, key, values):
        yield key, sum(values)

    def reducer(self, key, values):
        yield key, sum(values)

# input = [
#     "this is an example of this line",
#     "this is an example of some example text",
#     "this is another example",
#     "and this is some more text and text and text"
#     ]

with open("alice.txt","r") as f:
    input = f.read().lower().split()



output = WordCount().run(input)
max_key = ""
max_value = 0

uniques = []
for word in input:
  if word not in uniques:
    uniques.append(word)

counts = []
for unique in uniques:
  count = 0
  for word in input:
    if word == unique:
      count += 1
  counts.append((count, unique))
counts.sort()
counts.reverse()

for i in range(min(10, len(counts))):
  count, word = counts[i]
  print(i+1,'Most Common Word used---->',word,',Count--->', count)
counts.sort()
print('_______________________________________________________________')
for i in range(min(10, len(counts))):
  count, word = counts[i]
  print(i+1,'least Word used---->',word,',Count--->', count)