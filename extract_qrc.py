#!/usr/bin/env python3
import sys
from struct import unpack

# ota2
tree_offset = 0x015580
name_offset = 0x015780
data_offset = 0x016140

# ota1
tree_offset = 0x0D560
name_offset = 0x0D5C0
data_offset = 0x0D640

root_offset = 6
find_offset = lambda x: x * 14
tree_elem = (name_offset - tree_offset - root_offset) / find_offset(1)

def get_root(f):
  f.seek(tree_offset + root_offset)
  return unpack(">ii", f.read(8)) # (child_count, child)

def get_data(f, node):
  tree_node_offset = find_offset(node) + 4 #jump past name
  f.seek(tree_offset + tree_node_offset)
  flags = unpack(">h", f.read(2))[0]
  if flags & 2:
    return (None, flags, None)
  f.seek(tree_offset + tree_node_offset + 6)
  data_node_offset = unpack(">i", f.read(4))[0]
  f.seek(data_offset + data_node_offset)
  data_len = unpack(">i", f.read(4))[0]
  data = f.read(data_len)
  return (data, flags, data_len)

if __name__ == "__main__":
  if len(sys.argv) != 3:
    print("TODO")
    exit(1)
  with open(sys.argv[1], 'rb') as f:
    elem_n = int(sys.argv[2])
    if elem_n >= tree_elem:
      exit(1)
    data, flags, size  = get_data(f, elem_n)
    if len(data) == 0:
      exit(2)
    sys.stdout.buffer.write(data)
