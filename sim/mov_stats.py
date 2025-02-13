#! /usr/bin/env python3
# -*- coding: utf-8; tab-width: 2 -*-

from bisect import insort
from collections import deque
from random import randint, random
import heapq
import math
import numpy as np

class MovAvgStd:
  """
  >>> N_ITERS = 10
  >>> N_ELEMS = 1000
  >>> MIN_WINDOW = 1
  >>> MAX_WINDOW = 100
  >>> RANGES = [ (+10000000, +20000000),
  ...            (-20000000, -10000000),
  ...            (-10000000, +10000000) ]
  >>> for min_value, max_value in RANGES:
  ...   for iter in range(N_ITERS):
  ...     win_sz = randint(MIN_WINDOW, MAX_WINDOW)
  ...     comp = MovAvgStd(win_sz)
  ...     elems = np.zeros(N_ELEMS)
  ...     n_elems = 0
  ...     for n in range(N_ELEMS):
  ...       elems[n] = randint(min_value, max_value)
  ...       n_elems += 1
  ...       comp.add(elems[n])
  ...       cur_win_sz = min(win_sz, n_elems)
  ...       cur_win = elems[n_elems - cur_win_sz:n_elems]
  ...       target_avg = sum(cur_win) / cur_win_sz
  ...       target_var = sum([(x - target_avg)**2 / cur_win_sz for x in cur_win])
  ...       target_std = np.sqrt(target_var)
  ...       assert abs(target_avg - comp.mov_avg()) < 1
  ...       assert abs(target_var - comp.mov_var()) < 100
  ...       assert abs(target_std - comp.mov_std()) < 100
  """

  def __init__(self, win_len):
    self._window = deque(maxlen=win_len)
    self._sum = 0
    self._sum_squares = 0

  def mov_avg(self):
    return self._sum / len(self._window)

  def mov_var(self):
    avg = self.mov_avg()
    return self._sum_squares / len(self._window) - avg**2

  def mov_std(self):
    return np.sqrt(self.mov_var())

  def add(self, value):
    if len(self._window) == self._window.maxlen:
      old_value = self._window[0]
      self._sum -= old_value
      self._sum_squares -= old_value**2
    self._window.append(value)
    self._sum += value
    self._sum_squares += value**2

class MovMinMax:
  """
  >>> N_ITERS = 10
  >>> N_ELEMS = 1000
  >>> MIN_WINDOW = 1
  >>> MAX_WINDOW = 100
  >>> RANGES = [ (+10000000, +20000000),
  ...            (-20000000, -10000000),
  ...            (-10000000, +10000000) ]
  >>> for min_value, max_value in RANGES:
  ...   for iter in range(N_ITERS):
  ...     win_sz = randint(MIN_WINDOW, MAX_WINDOW)
  ...     comp = MovMinMax(win_sz)
  ...     elems = np.zeros(N_ELEMS)
  ...     n_elems = 0
  ...     for n in range(N_ELEMS):
  ...       elems[n] = randint(min_value, max_value)
  ...       n_elems += 1
  ...       comp.add(elems[n])
  ...       cur_win_sz = min(win_sz, n_elems)
  ...       cur_win = elems[n_elems - cur_win_sz:n_elems]
  ...       target_min = min(cur_win)
  ...       target_max = max(cur_win)
  ...       assert target_min == comp.mov_min()
  ...       assert target_max == comp.mov_max()
  """

  def __init__(self, win_len):
    self._window = deque(maxlen=win_len)
    self._min_heap = []
    self._max_heap = []

  def mov_min(self):
    return self._min_heap[0]

  def mov_max(self):
    return -self._max_heap[0]

  def add(self, value):
    self._window.append(value)
    heapq.heappush(self._min_heap, value)
    heapq.heappush(self._max_heap, -value)
    while self._min_heap[0] not in self._window:
      heapq.heappop(self._min_heap)
    while -self._max_heap[0] not in self._window:
      heapq.heappop(self._max_heap)

class MovQuantile:
  """
  >>> N_ITERS = 10
  >>> N_ELEMS = 1000
  >>> MIN_WINDOW = 1
  >>> MAX_WINDOW = 100
  >>> for iter in range(N_ITERS):
  ...   win_sz = randint(MIN_WINDOW, MAX_WINDOW)
  ...   quant = random()
  ...   comp = MovQuantile(win_sz, quant)
  ...   elems = np.zeros(N_ELEMS)
  ...   n_elems = 0
  ...   for n in range(N_ELEMS):
  ...     elems[n] = random()
  ...     n_elems += 1
  ...     comp.add(elems[n])
  ...     cur_win_sz = min(win_sz, n_elems)
  ...     cur_win = np.copy(elems[n_elems - cur_win_sz:n_elems])
  ...     cur_win.sort()
  ...     cur_win_mid = int(np.floor((cur_win_sz - 1) * quant))
  ...     expected = cur_win[cur_win_mid]
  ...     actual = comp.mov_quantile()
  ...     assert abs(expected - actual) < 0.00001
  """

  def __init__(self, win_len, quantile):
    self._quantile = quantile
    self._window = deque(maxlen=win_len)
    self._sorted = []

  def mov_quantile(self):
    if not self._sorted:
      return 0
    idx = int(self._quantile * (len(self._sorted)-1))
    return self._sorted[idx]

  def add(self, value):
    if len(self._window) == self._window.maxlen:
      old = self._window[0]
      self._window.append(value)
      self._sorted.remove(old)
      insort(self._sorted, value)
    else:
      self._window.append(value)
      insort(self._sorted, value)
