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
