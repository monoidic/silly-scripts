#!/usr/bin/env python3


def get_fib_period(m):
  period = []
  previous, current = 0, 1
  while True:
    period.append(previous)
    previous, current = current, (previous + current) % m
    if previous == 0 and current == 1:
      break # period found

  return period


def fib_sum_slow(n, m):
  total = 0
  previous, current = 0, 1

  for _ in range(n):
    previous, current = current, (previous + current) % m
    total = (total + previous) % m

  return total


def fib_sum_fast(n, m):
  period = get_fib_period(m)
  per_period_sum = sum(period) % m

  return sum(period[:(n % len(period))+1]) % m


for MOD in range(2, 1000):
  print(f'{MOD=}')
  for i in range(2, 1000):
    correct = fib_sum_slow(i, MOD)
    assumed = fib_sum_fast(i, MOD)
    if assumed != correct:
      print(f'{i=}: {assumed=}, {correct=}')
