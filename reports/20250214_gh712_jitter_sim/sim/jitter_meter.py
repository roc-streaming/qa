#! /usr/bin/env python3
# -*- coding: utf-8; tab-width: 2 -*-

from dataclasses import dataclass
import numpy as np
import sys

if 'pytest' in sys.modules:
  from .mov_stats import *

@dataclass
class JitterMeterConfig:
  jitter_window: int = 50000
  envelope_smoothing_window_len: int = 10
  envelope_resistance_exponent: float = 6.0
  envelope_resistance_coeff: float = 0.1
  peak_quantile_window: int = 10000
  peak_quantile_coeff: float = 0.92

@dataclass
class JitterMetrics:
  mean_jitter: float = 0
  peak_jitter: float = 0
  curr_jitter: float = 0
  curr_envelope: float = 0

class JitterMeterA:
  """
  >>> meter = JitterMeterA()
  >>> meter.update_jitter(1000)
  >>> meter.update_jitter(1500)
  >>> meter.update_jitter(1000)
  >>> meter.metrics()
  JitterMetrics(mean_jitter=1167, peak_jitter=1500, curr_jitter=1000, curr_envelope=1500)
  """

  def __init__(self, config=None):
    if not config:
      config = JitterMeterConfig()
    self._config = config
    self._metrics = JitterMetrics()
    self._jitter_window = MovAvgStd(config.jitter_window)
    self._smooth_jitter_window = MovMinMax(config.envelope_smoothing_window_len)
    self._envelope_window = MovQuantile(config.peak_quantile_window,
                                        config.peak_quantile_coeff)
    self._peak_window = MovMinMax(config.jitter_window)
    self._capacitor_charge = 0
    self._capacitor_discharge_resistance = 0
    self._capacitor_discharge_iteration = 0

  def metrics(self):
    return self._metrics

  def update_jitter(self, jitter):
    self._jitter_window.add(jitter)

    self._smooth_jitter_window.add(jitter)
    jitter_envelope = self._update_envelope(
        self._smooth_jitter_window.mov_max(), self._jitter_window.mov_avg())

    self._envelope_window.add(jitter_envelope)
    self._peak_window.add(self._envelope_window.mov_quantile())

    self._metrics.mean_jitter = round(self._jitter_window.mov_avg())
    self._metrics.peak_jitter = round(self._peak_window.mov_max())
    self._metrics.curr_jitter = round(jitter)
    self._metrics.curr_envelope = round(jitter_envelope)

  def _update_envelope(self, cur_jitter, avg_jitter):
    if self._capacitor_charge < cur_jitter:
      self._capacitor_charge = cur_jitter
      self._capacitor_discharge_resistance = math.pow(
        cur_jitter / avg_jitter,
        self._config.envelope_resistance_exponent) * self._config.envelope_resistance_coeff
      self._capacitor_discharge_iteration = 0
    elif self._capacitor_charge > 0:
      self._capacitor_charge *= math.exp(
        -self._capacitor_discharge_iteration / self._capacitor_discharge_resistance)
      self._capacitor_discharge_iteration += 1
    if self._capacitor_charge < 0:
      self._capacitor_charge = 0
    return self._capacitor_charge

def sim_jitter_meter(algo, jitter):
  jm = algo()

  peak_jitter = np.zeros_like(jitter)
  for i in range(len(jitter)):
    jm.update_jitter(jitter[i])
    peak_jitter[i] = jm.metrics().peak_jitter

  return peak_jitter
