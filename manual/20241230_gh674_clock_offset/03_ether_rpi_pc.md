# Table of Contents

1.  [Test summary](#org298eced)
2.  [Setup code](#orgd233bb2)
3.  [Round Trip Time](#orgd5c2f38)
4.  [Clock Offset](#org9ebafa0)


<a id="org298eced"></a>

# Test summary


## Environment

-   **Devices**
    -   Sender: RPi4B (`arm32`)
    -   Receiver: PC (`x86_64`)

-   **Network**
    -   Ethernet (direct connection)

-   **Audio**
    -   input and output are WAV files

-   **Ping**
    -   below 0.3ms

-   **Scheduling**
    -   `SCHED_RR` disabled


## Info

-   **Git revisions**
    
    ```
    cd ~/dev/roc-streaming/roc-toolkit && git log -1 --format=short
    ```
    
        commit 5e8528929835d8c8844ce3fd020047373488e6ab
        Author: Mikhail Baranov <baranov.mv@gmail.com>
        
            Slot provides Control endpoints ts
    
    ```
    cd ~/dev/roc-streaming/csvplotter && git log -1 --format=short
    ```
    
        commit 1ef0a47962b9071c2cc76175c59179ddf7895d12
        Author: Mikhail Baranov <baranov.mv@gmail.com>
        
            plot t1-t4 stats

-   **Estimate clock offset**
    
    Rough difference between unix time on two machines.
    
    ```
    ssh raspberrypi-4b.eth "date -u +%s" | awk -v local="$(date -u +%s)" '{print local - $1}'
    ```
    
        11798932

-   **Estimate ping**
    
    ```
    ping -q -i 0.002 -c 1000 raspberrypi-4b.eth
    ```
    
        PING raspberrypi-4b.eth (192.168.2.131) 56(84) bytes of data.
        
        --- raspberrypi-4b.eth ping statistics ---
        1000 packets transmitted, 1000 received, 0% packet loss, time 1996ms
        rtt min/avg/max/mdev = 0.119/0.149/0.250/0.025 ms


## Running

-   **stop ntpd**
    
    ```
    sudo systemctl stop ntp
    ```

-   **run roc-send**
    
    ```
    ./roc-send -vv -s rtp+rs8m://dell-xps15.eth:10001 -r rs8m://dell-xps15.eth:10002 -c rtcp://dell-xps15.eth:10003 -i file:long.wav
    ```

-   **run roc-recv**
    
    ```
    ./roc-recv -vv -s rtp+rs8m://0.0.0.0:10001 -r rs8m://0.0.0.0:10002 -c rtcp://0.0.0.0:10003 -o file:test.wav --dump test.csv
    ```

-   **run csvplotter**
    
    ```
    python3 ./csvplotter.py test.csv
    ```


<a id="orgd233bb2"></a>

# Setup code

<details>
  <summary>Click to expand</summary>

```python
%matplotlib inline
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import os
import subprocess

plt.rcParams['figure.figsize'] = [20, 10]
plt.rcParams['figure.dpi'] = 100
plt.rcParams.update({'font.size': 24})
plt.style.use(['dark_background'])

def load_csv(path):
  if os.path.exists(path):
    iterator = open(path)
  else:
    iterator = (line.decode('utf-8') for line in
                subprocess.Popen(['xz', '-dc', f'{path}.xz'],
                                 stdout=subprocess.PIPE).stdout)

  lines = []
  for line in iterator:
    if not line.startswith('r,'):
      continue
    lines.append(line.replace('r,', '').strip())

  data = np.genfromtxt(lines, dtype=float, delimiter=',')
  data[:,0] /= 1e9
  data[:,0] -= data[0,0]
  for n in range(1, data.shape[1]):
    data[:,n] /= 1e9

  return data

def configure_plot():
  ax = plt.gca()
  ax.grid(True)
  ax.ticklabel_format(useOffset=False, style='plain')
  ax.get_yaxis().set_major_formatter(ticker.FuncFormatter(
    lambda x, pos: "{:,.3f}".format(x).replace(",", "'")))

def print_stats(name, values):
  values = values * 1000
  print("""
{} statistics:
  min:  {:.3f} ms
  max:  {:.3f} ms
  avg:  {:.3f} ms
  p95:  {:.3f} ms
  """.format(
    name,
    np.min(values),
    np.max(values),
    np.mean(values),
    np.percentile(values, 95)).lstrip())

def print_jitter(name, values):
  values = values * 1000
  jitter = np.abs(np.diff(np.diff(values)))
  print("""
{} jitter:
  min:  {:.3f} ms
  max:  {:.3f} ms
  avg:  {:.3f} ms
  p95:  {:.3f} ms
  """.format(
    name,
    np.min(jitter),
    np.max(jitter),
    np.mean(jitter),
    np.percentile(jitter, 95)).lstrip())

def print_drift(name, tstamps, values):
  tstamp_delta = tstamps[-1] - tstamps[0]
  values_delta = values[-1] - values[0]
  values_drift = values_delta / tstamp_delta
  print("""
{} drift:
  {:.6f} sec/sec
  {:.3f} sec/day
  """.format(
    name,
    values_drift,
    values_drift * 60 * 60 * 24).lstrip())
```

</details>

```python
data = load_csv('03_ether_rpi_pc.csv')
data = data[1:,]
```

    # Out[84]:


<a id="orgd5c2f38"></a>

# Round Trip Time


## Overall

```python
plt.plot(data[:,0]/60, data[:,1]*1000)
plt.legend(['rtt, ms'], labelcolor='linecolor')
configure_plot()
```

<img width="700px" src="images/ItF268.gif"/>


## Zoomed

```python
plt.plot(data[550:600,0]/60, data[550:600,1]*1000)
plt.legend(['rtt, ms'], labelcolor='linecolor')
configure_plot()
```

<img width="700px" src="images/g4CACo.gif"/>


## Statistics

```python
print_stats("RTT", data[:,1])
print_jitter("RTT", data[:,1])
```

```
RTT statistics:
  min:  0.356 ms
  max:  0.529 ms
  avg:  0.462 ms
  p95:  0.508 ms
  
RTT jitter:
  min:  0.000 ms
  max:  0.169 ms
  avg:  0.010 ms
  p95:  0.037 ms
  
```


<a id="org9ebafa0"></a>

# Clock Offset


## Overall

```python
plt.plot(data[:,0]/60, data[:,2], 'C5')
plt.legend(['clock_offset, sec'], labelcolor='linecolor')
configure_plot()
```

<img width="700px" src="images/Vl6xxc.gif"/>


## Zoomed

```python
plt.plot(data[550:600,0]/60, data[550:600,2]*1000, 'C5')
plt.legend(['clock_offset, ms'], labelcolor='linecolor')
configure_plot()
```

<img width="700px" src="images/PQH2wP.gif"/>


## Statistics

```python
print_drift("Clock offset", data[:,0], data[:,2])
print_jitter("Clock offset", data[:,2])
```

```
Clock offset drift:
  0.000016 sec/sec
  1.378 sec/day
  
Clock offset jitter:
  min:  0.000 ms
  max:  0.038 ms
  avg:  0.003 ms
  p95:  0.010 ms
  
```
