#! /usr/bin/env python3
# -*- coding: utf-8; tab-width: 2 -*-

from random import randint, random
import numpy as np

class MovQuantileHeap:
  """
  >>> N_ITERS = 10
  >>> N_ELEMS = 1000
  >>> MIN_WINDOW = 1
  >>> MAX_WINDOW = 100
  >>> for iter in range(N_ITERS):
  ...   win_sz = randint(MIN_WINDOW, MAX_WINDOW)
  ...   quant = random()
  ...   comp = MovQuantileHeap(win_sz, quant)
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
    self._win_len = win_len
    self._quantile = quantile

    self._old_heap_root_index = 0
    self._heap_root = 0
    self._heap_size = 0
    self._max_heap_index = 0
    self._min_heap_index = 0
    self._elem_index = 0
    self._heap = np.zeros(win_len)
    self._elem_index_2_heap_index = np.zeros(win_len, int)
    self._heap_index_2_elem_index = np.zeros(win_len, int)

    self._heap_root = int(quantile * float(win_len - 1))
    self._max_heap_index = self._heap_root
    self._min_heap_index = self._heap_root

  def mov_quantile(self):
    return self._heap[self._heap_root]

  def add(self, x):
    win_filled = (self._heap_size == self._win_len)
    if self._heap_size < self._win_len:
      self._heap_size += 1

    if win_filled:
      heap_index = self._elem_index_2_heap_index[self._elem_index]
      self._heap[heap_index] = x
      self._heapify(heap_index)
    else:
      k = int(self._quantile * float(self._heap_size - 1))
      if self._elem_index == 0:
        heap_index = self._heap_root
        self._elem_index_2_heap_index[self._elem_index] = heap_index
        self._heap[heap_index] = x
        self._heap_index_2_elem_index[heap_index] = self._elem_index
      else:
        if self._old_heap_root_index == k:
          self._min_heap_index += 1
          heap_index = self._min_heap_index
        else:
          self._max_heap_index -= 1
          heap_index = self._max_heap_index
        self._elem_index_2_heap_index[self._elem_index] = heap_index
        self._heap[heap_index] = x
        self._heap_index_2_elem_index[heap_index] = self._elem_index
        self._heapify(heap_index)
        self._old_heap_root_index = k

    self._elem_index = (self._elem_index + 1) % self._win_len

  def _heapify(self, heap_index):
    if heap_index < self._heap_root:
      parent = self._heap_root - ((self._heap_root - heap_index - 1) // 2)
      if self._heap[parent] < self._heap[heap_index]:
        self._max_heapify_up(heap_index)
        self._min_heapify_down(self._heap_root)
      else:
        self._max_heapify_down(heap_index)
    elif self._heap_root == heap_index:
      self._max_heapify_down(heap_index)
      self._min_heapify_down(self._heap_root)
    else:
      parent = (heap_index - self._heap_root - 1) // 2 + self._heap_root
      if self._heap[parent] > self._heap[heap_index]:
        self._min_heapify_up(heap_index)
        self._max_heapify_down(self._heap_root)
      else:
        self._min_heapify_down(heap_index)

  def _min_heapify_up(self, heap_index):
    if heap_index == self._heap_root:
      return
    parent = (heap_index - self._heap_root - 1) // 2 + self._heap_root
    if self._heap[parent] > self._heap[heap_index]:
      self._swap(heap_index, parent)
      self._min_heapify_up(parent)

  def _max_heapify_up(self, heap_index):
    if heap_index == self._heap_root:
      return
    parent = self._heap_root - ((self._heap_root - heap_index - 1) // 2)
    if self._heap[parent] < self._heap[heap_index]:
      self._swap(heap_index, parent)
      self._max_heapify_up(parent)

  def _min_heapify_down(self, heap_index):
    largest = heap_index

    left = 2 * (heap_index - self._heap_root) + 1 + self._heap_root
    if left <= self._min_heap_index and self._heap[left] < self._heap[largest]:
      largest = left
    right = 2 * (heap_index - self._heap_root) + 2 + self._heap_root
    if right <= self._min_heap_index and self._heap[right] < self._heap[largest]:
      largest = right

    if largest != heap_index:
      self._swap(heap_index, largest)
      self._min_heapify_down(largest)

  def _max_heapify_down(self, heap_index):
    largest = heap_index

    left = 2 * (self._heap_root - heap_index) + 1
    if left <= (self._heap_root - self._max_heap_index) and \
       self._heap[self._heap_root - left] > self._heap[largest]:
      largest = self._heap_root - left
    right = 2 * (self._heap_root - heap_index) + 2
    if right <= (self._heap_root - self._max_heap_index) and \
       self._heap[self._heap_root - right] > self._heap[largest]:
      largest = self._heap_root - right
    if largest != heap_index:
      self._swap(heap_index, largest)
      self._max_heapify_down(largest)

  def _swap(self, index_1, index_2):
    elem_index_1 = self._heap_index_2_elem_index[index_1]
    elem_index_2 = self._heap_index_2_elem_index[index_2]

    temp = self._heap[index_1]
    self._heap[index_1] = self._heap[index_2]
    self._heap[index_2] = temp

    self._heap_index_2_elem_index[index_1] = elem_index_2
    self._heap_index_2_elem_index[index_2] = elem_index_1

    self._elem_index_2_heap_index[elem_index_1] = index_2
    self._elem_index_2_heap_index[elem_index_2] = index_1
