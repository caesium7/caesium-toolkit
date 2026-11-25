import math

def quadratic():
  a = float(input('Enter a from your quadratic (ax² + bx + c = 0): '))
  b = float(input('Enter b from your quadratic (ax² + bx + c = 0): '))
  c = float(input('Enter c from your quadratic (ax² + bx + c = 0): '))

  if a == 0:
    print("If 'a' is 0, this is a linear equation, not a quadratic.")
    return

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
  elif f == 0:
    print('Quadratic has one real root. Proceeding to solve...')
    p = h / g
    print(f'x = {p}.')
  else:
    print('Quadratic has no real roots. Use imag_quadratic()')
