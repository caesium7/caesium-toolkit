import math
import cmath


def quadratic(a=None, b=None, c=None):
  """Solves a quadratic equation ax² + bx + c = 0 for real roots."""
  if a is None:
    a = float(input('Enter a from your quadratic (ax² + bx + c = 0): '))
  if b is None:
    b = float(input('Enter b from your quadratic (ax² + bx + c = 0): '))
  if c is None:
    c = float(input('Enter c from your quadratic (ax² + bx + c = 0): '))

  if a == 0:
    print("If 'a' is 0, this is a linear equation, not a quadratic.")
    return None

  d = b ** 2
  e = 4 * a * c
  f = d - e
  g = 2 * a
  h = -1 * b

  if f > 0:
    print('Quadratic has two real roots. Proceeding to solve...')
    k = math.sqrt(f)
    l = (h + k) / g
    m = (h - k) / g
    print(f'x = {l} or {m}.')
    return l, m
  elif f == 0:
    print('Quadratic has one real root. Proceeding to solve...')
    p = h / g
    print(f'x = {p}.')
    return p
  else:
    print('Quadratic has no real roots. Use imag_quadratic()')
    return None


def imag_quadratic(a=None, b=None, c=None):
  """Solves a quadratic equation ax² + bx + c = 0 for imaginary roots."""
  if a is None:
    a = float(input('Enter a from your quadratic (ax² + bx + c = 0): '))
  if b is None:
    b = float(input('Enter b from your quadratic (ax² + bx + c = 0): '))
  if c is None:
    c = float(input('Enter c from your quadratic (ax² + bx + c = 0): '))

  if a == 0:
    print("If 'a' is 0, this is a linear equation, not a quadratic.")
    return None

  d = b ** 2
  e = 4 * a * c
  f = d - e
  g = 2 * a
  h = -1 * b

  if f >= 0:
    print('Quadratic has real roots. Use quadratic()')
    return None
  else:
    print('Quadratic has two imaginary roots. Proceeding to solve...')
    k = cmath.sqrt(f)
    l = (h + k) / g
    m = (h - k) / g
    print(f'x = {l} or {m}.')
    return l, m


def factors(x=None):
  """Prints and returns a list of all positive factors of x."""
  if x is None:
    x = int(input('Input the number whose factors will be displayed: '))

  y = []
  for i in range(1, x + 1):
    if x % i == 0:
      y.append(i)

  print(y)
  return y


def is_prime(x=None):
  """Checks if x is a prime number, printing and returning True or False."""
  if x is None:
    x = int(input('Input a number to check if it is prime: '))

  result = x >= 2 and len(factors(x)) == 2
  print(result)
  return result
import cmath
import math


def cubic(a=None, b=None, c=None, d=None):
  """Solves a cubic equation ax³ + bx² + cx + d = 0 for all three roots."""
  if a is None:
    a = float(input('Enter a from your cubic (ax³ + bx² + cx + d = 0): '))
  if b is None:
    b = float(input('Enter b from your cubic (ax³ + bx² + cx + d = 0): '))
  if c is None:
    c = float(input('Enter c from your cubic (ax³ + bx² + cx + d = 0): '))
  if d is None:
    d = float(input('Enter d from your cubic (ax³ + bx² + cx + d = 0): '))

  if a == 0:
    print("If 'a' is 0, this is not a cubic.")
    return None

  s = b / (3 * a)
  t = 3 * a * c - b**2
  p = t / (3 * a**2)

  w = 2 * (b**3) - 9 * a * b * c + 27 * (a**2) * d
  q = w / (27 * (a**3))

  delta = (q / 2) ** 2 + (p / 3) ** 3

  if delta > 1e-12:
    print(
        'Cubic has one real root and two complex roots. Proceeding to solve...'
    )
    sqrt_delta = math.sqrt(delta)
    u = math.cbrt(-q / 2 + sqrt_delta)
    v = math.cbrt(-q / 2 - sqrt_delta)

    x1 = round((u + v) - s, 10) + 0.0
    real_part = round(-0.5 * (u + v) - s, 10) + 0.0
    imag_part = round((math.sqrt(3) / 2) * (u - v), 10) + 0.0

    x2 = complex(real_part, imag_part)
    x3 = complex(real_part, -imag_part + 0.0)
    print(f'x = {x1}, {x2}, or {x3}.')
    return x1, x2, x3

  elif abs(delta) <= 1e-12:
    if abs(p) < 1e-12 and abs(q) < 1e-12:
      print('Cubic has one triple real root. Proceeding to solve...')
      x1 = round(-s, 10) + 0.0
      print(f'x = {x1}.')
      return x1, x1, x1
    else:
      print('Cubic has repeated real roots. Proceeding to solve...')
      x1 = round((3 * q / p) - s, 10) + 0.0
      x2 = round((-3 * q / (2 * p)) - s, 10) + 0.0
      print(f'x = {x1} or {x2} (double root).')
      return x1, x2, x2

  else:
    print('Cubic has three distinct real roots. Proceeding to solve...')
    r = 2 * math.sqrt(-p / 3)
    cos_val = (3 * q) / (2 * p) * math.sqrt(-3 / p)
    cos_val = max(-1.0, min(1.0, cos_val))
    theta = math.acos(cos_val) / 3

    x1 = round(r * math.cos(theta) - s, 10) + 0.0
    x2 = round(r * math.cos(theta - (2 * math.pi / 3)) - s, 10) + 0.0
    x3 = round(r * math.cos(theta - (4 * math.pi / 3)) - s, 10) + 0.0
    print(f'x = {x1}, {x2}, or {x3}.')
    return x1, x2, x3
  
