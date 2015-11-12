#!/usr/bin/python
import sys
import random
from lxml import etree

def shape_area(shape):
  # todo
  return 1

class Shape:
  def __init__(self, shape):
    xmin, xmax, ymin, ymax = None, None, None, None
    for coord in shape:
      if coord is None:
        continue
      if xmin is None or coord[0] < xmin:
        xmin = coord[0]
      if xmax is None or coord[0] > xmax:
        xmax = coord[0]
      if ymin is None or coord[1] < ymin:
        ymin = coord[1]
      if ymax is None or coord[1] > ymax:
        ymax = coord[1]
    self.valid = xmin is not None
    if self.valid:
      self.width = xmax - xmin
      self.height = ymax - ymin
      self.bbarea = self.width * self.height
      self.area = shape_area(shape)
      self.shape = []
      for coord in shape:
        self.shape.append(None if coord is None else (coord[0] - xmin, coord[1] - ymin))

  def __repr__(self):
    return '{0}: {1}'.format(self.area, repr(self.shape))

  def scaled(self, scale):
    for coord in self.shape:
      yield (coord[0] * scale, coord[1] * scale)

def process_shapes(shapes):
  """Convert a list of coord lists to a sorted list of Shape objects."""
  result = []
  for shape in shapes:
    s = Shape(shape)
    if s.valid:
      result.append(s)
  result.sort(key=lambda s: s.bbarea, reverse=True)
  return result

def xml_to_geometry(f):
  # Read all nodes
  # Store all ways as coord arrays in a dict
  # Complete multipolygon relaions to shapes
  # Unused closed ways to shapes
  for _, element in etree.iterparse(f):
    pass

def create_random():
  result = []
  for i in range(random.randrange(100)):
    w = random.random() * 100
    h = random.random() * 100
    result.append([(0, 0), (0, h), (w, h), (w, 0)])
  return result

def center_row(row, width):
  return row

def fit_in_width(shapes, width, gap):
  """Returns an array of top-left coordinates for each feature (0,0 = top left)."""
  result = []
  row = []
  x = 0
  y = 0
  height = 0
  for shape in shapes:
    if len(row) > 0 and x + shape.width > width:
      dx = (width - x + gap) / 2
      for rx in row:
        result.append((rx + dx, y))
      row = []
      x = 0
      y += height + gap
      height = 0
    row.append(x)
    x += shape.width + gap
    height = max(height, shape.height)
  if len(row) > 0:
    dx = (width - x + gap) / 2
    for rx in row:
      result.append((rx + dx, y))
  return result

def fit_on_page(shapes, width_to_height, gap):
  """Returns an array of top-left coordinates for each feature (0,0 = top left)."""
  return []

def shapes_to_svg(shapes, positions, xmin, ymin, xmax, ymax):
  """Returns an array of XML strings for SVG. Scales all features to fit into given coords."""
  return []

if __name__ == "__main__":
  if len(sys.argv) < 2:
    print 'Usage: {0} <source.osm>'.format(sys.argv[0])
    sys.exit(1)

  print 'Sources are not yet read, using random'
  data = create_random()
  shapes = process_shapes(data)
  if len(shapes) == 0:
    print 'No shapes in the source file'
    sys.exit(1)

  width = 210 * 3.543307
  height = 297 * 3.543307
  positions = fit_on_page(shapes, width / height, 10)
  svg_shapes = shapes_to_svg(shapes, positions, 100, 100, width - 100, height - 100)
  for l in svg_shapes:
    print l
