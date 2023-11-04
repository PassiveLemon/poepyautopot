class Meter(object):
  def __init__(self, name, enable, pixel, empty, need):
    self.name = name
    self.enable = enable
    self.pixel = pixel
    self.empty = empty
    self.need = need
  def __str__(self):
    return self.name

class Flask(object):
  def __init__(self, name, number, enable, offset_x, type, pixel, empty, duration, react, always, valid, lock):
    self.name = name
    self.number = number
    self.enable = enable
    self.offset_x = offset_x
    self.type = type
    self.pixel = pixel
    self.empty = empty
    self.duration = duration
    self.react = react
    self.always = always
    self.valid = valid
    self.lock = lock
  def __str__(self):
    return self.name

class Menu(object):
  def __init__(self, name, pixel1, pixel2, pixel3, color1, color2, color3, inside):
    self.name = name
    self.pixel1 = pixel1
    self.pixel2 = pixel2
    self.pixel3 = pixel3
    self.color1 = color1
    self.color2 = color2
    self.color3 = color3
    self.inside = inside
  def __str__(self):
    return self.name
