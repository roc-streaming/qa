# TOC

<!-- toc -->

- [Description](#description)
  * [Test matrix](#test-matrix)
  * [Hardware](#hardware)
  * [Software](#software)
- [Tests](#tests)
  * [Case 01: `good_wifi--no_load--gradual_profile`](#case-01-good_wifi--no_load--gradual_profile)
  * [Case 02: `good_wifi--no_load--responsive_profile`](#case-02-good_wifi--no_load--responsive_profile)
  * [Case 03: `good_wifi--medium_load--gradual_profile`](#case-03-good_wifi--medium_load--gradual_profile)
  * [Case 04: `good_wifi--high_load--gradual_profile`](#case-04-good_wifi--high_load--gradual_profile)
  * [Case 05: `bad_wifi--no_load--gradual_profile`](#case-05-bad_wifi--no_load--gradual_profile)
  * [Case 06: `bad_wifi--low_load--gradual_profile`](#case-06-bad_wifi--low_load--gradual_profile)
  * [Case 07: `ethernet--default_latency--responsive_profile`](#case-07-ethernet--default_latency--responsive_profile)
  * [Case 08: `ethernet--low_latency--responsive_profile`](#case-08-ethernet--low_latency--responsive_profile)
  * [Case 09: `internet--gradual_profile`](#case-09-internet--gradual_profile)

<!-- tocstop -->

# Description

Testing how adaptive latency behaves in different conditions.

Github issue: [gh-688](https://github.com/roc-streaming/roc-toolkit/issues/688).

## Test matrix

Network:

- Wi-Fi (good)
- Wi-Fi (bad)
- Ethernet
- Internet (VPN)

Artificial load:

* none
* small (200 pkt/sec)
* medium (1000 pkt/sec)
* high (2000 pkt/sec)
* very high (10000 pkt/sec)

Profile:

- responsive
- gradual

## Hardware

- Sender: laptop
- Receiver: RPi-4B
- Wi-Fi (good): 5ghz, short range
- Wi-Fi (bad): 2ghz, 7m range, poor signal
- Ethernet: direct connection
- Internet: loopback over VPN with 100ms ping

## Software

- roc-toolkit pre-0.5
- csvplotter a97b1d474581bad3ca62f809ed8589f29f4cfb2e (+ patches)
- hping3 for simulating network load

# Tests

## Case 01: `good_wifi--no_load--gradual_profile`

Verdict: **good**

Summary:

* peak jitter: start at 80ms, stabilized at 140ms
* target latency: remained at 200ms
* losses: none

Sender:

```
roc-send -vv -s rtp+rs8m://raspberrypi-4b-ubuntu.lan:20001 -r rs8m://raspberrypi-4b-ubuntu.lan:20002 \
   -c rtcp://raspberrypi-4b-ubuntu.lan:20003 -i pulse://null.monitor
```

Receiver:

```
roc-recv -vv -s rtp+rs8m://0.0.0.0:20001 -r rs8m://0.0.0.0:20002 -c rtcp://0.0.0.0:20003 \
   -o pulse://default --plc=beep --latency-profile=gradual --dump /tmp/dump.csv
```

Measurements:

[**dump.csv.xz**](01--good_wifi--no_load--gradual_profile/dump.csv.xz)

<table>
  <tr>
    <td><img width="160px" src="01--good_wifi--no_load--gradual_profile/screenshot_01.gif"/></td>
    <td><img width="160px" src="01--good_wifi--no_load--gradual_profile/screenshot_02.gif"/></td>
    <td><img width="160px" src="01--good_wifi--no_load--gradual_profile/screenshot_03.gif"/></td>
    <td><img width="160px" src="01--good_wifi--no_load--gradual_profile/screenshot_04.gif"/></td>
    <td><img width="160px" src="01--good_wifi--no_load--gradual_profile/screenshot_05.gif"/></td>
  </tr>
</table>

## Case 02: `good_wifi--no_load--responsive_profile`

Verdict: **good**

Summary:

* peak jitter: started at 60ms, reached 140ms, stabilized at 100ms
* target latency: reached 240ms, stabilized at 150ms
* losses: none

Sender:

```
roc-send -vv -s rtp+rs8m://raspberrypi-4b-ubuntu.lan:20001 -r rs8m://raspberrypi-4b-ubuntu.lan:20002 \
   -c rtcp://raspberrypi-4b-ubuntu.lan:20003 -i pulse://null.monitor
```

Receiver:

```
roc-recv -vv -s rtp+rs8m://0.0.0.0:20001 -r rs8m://0.0.0.0:20002 -c rtcp://0.0.0.0:20003 \
   -o pulse://default --plc=beep --latency-profile=responsive --dump /tmp/dump.csv
```

Measurements:

[**dump.csv.xz**](02--good_wifi--no_load--responsive_profile/dump.csv.xz)

<table>
  <tr>
    <td><img width="160px" src="02--good_wifi--no_load--responsive_profile/screenshot_01.gif"/></td>
    <td><img width="160px" src="02--good_wifi--no_load--responsive_profile/screenshot_02.gif"/></td>
    <td><img width="160px" src="02--good_wifi--no_load--responsive_profile/screenshot_03.gif"/></td>
    <td><img width="160px" src="02--good_wifi--no_load--responsive_profile/screenshot_04.gif"/></td>
    <td><img width="160px" src="02--good_wifi--no_load--responsive_profile/screenshot_05.gif"/></td>
    <td><img width="160px" src="02--good_wifi--no_load--responsive_profile/screenshot_06.gif"/></td>
  </tr>
</table>

## Case 03: `good_wifi--medium_load--gradual_profile`

Verdict: **good**

Summary:

* peak jitter: started at 60ms, increased to 200ms under load, decreased to 140ms without load
* target latency: increased to 260ms under load, decreased to 210ms without load
* losses: lost 120ms, FEC didn't help

Sender:

```
roc-send -vv -s rtp+rs8m://raspberrypi-4b-ubuntu.lan:20001 -r rs8m://raspberrypi-4b-ubuntu.lan:20002 \
   -c rtcp://raspberrypi-4b-ubuntu.lan:20003 -i pulse://null.monitor
```

Receiver:

```
roc-recv -vv -s rtp+rs8m://0.0.0.0:20001 -r rs8m://0.0.0.0:20002 -c rtcp://0.0.0.0:20003 \
   -o pulse://default --plc=beep --latency-profile=gradual --dump /tmp/dump.csv
```

Load (1000 pkt/sec):

```
sudo hping3 -i u1000 -S -p 80 raspberrypi-4b-ubuntu.lan
```

Measurements:

[**dump.csv.xz**](03--good_wifi--medium_load--gradual_profile/dump.csv.xz)

<table>
  <tr>
    <td><img width="160px" src="03--good_wifi--medium_load--gradual_profile/screenshot_01.gif"/></td>
    <td><img width="160px" src="03--good_wifi--medium_load--gradual_profile/screenshot_02.gif"/></td>
    <td><img width="160px" src="03--good_wifi--medium_load--gradual_profile/screenshot_03.gif"/></td>
    <td><img width="160px" src="03--good_wifi--medium_load--gradual_profile/screenshot_04.gif"/></td>
  </tr>
  <tr>
    <td></td>
    <td>load enabled</td>
    <td></td>
    <td>load disabled (+ 2 minutes wait)</td>
  </tr>
</table>

## Case 04: `good_wifi--high_load--gradual_profile`

Verdict: **good**

Summary:

* peak jitter: started at 60ms, increased to 220ms under load, decreased to 120ms without load
* target latency: increased to 300ms under load, decreased to 200ms without load
* losses: none

Sender:

```
roc-send -vv -s rtp+rs8m://raspberrypi-4b-ubuntu.lan:20001 -r rs8m://raspberrypi-4b-ubuntu.lan:20002 \
   -c rtcp://raspberrypi-4b-ubuntu.lan:20004 -i pulse://null.monitor
```

Receiver:

```
roc-recv -vv -s rtp+rs8m://0.0.0.0:20001 -r rs8m://0.0.0.0:20002 -c rtcp://0.0.0.0:20004 \
   -o pulse://default --plc=beep --latency-profile=gradual --dump /tmp/dump.csv
```

Load (2000 pkt/sec):

```
sudo hping3 -i u500 -S -p 80 raspberrypi-4b-ubuntu.lan
```

Measurements:

*no dump*

<table>
  <tr>
    <td><img width="160px" src="04--good_wifi--high_load--gradual_profile/screenshot_01.gif"/></td>
    <td><img width="160px" src="04--good_wifi--high_load--gradual_profile/screenshot_02.gif"/></td>
    <td><img width="160px" src="04--good_wifi--high_load--gradual_profile/screenshot_03.gif"/></td>
    <td><img width="160px" src="04--good_wifi--high_load--gradual_profile/screenshot_04.gif"/></td>
  </tr>
  <tr>
    <td></td>
    <td>load enabled</td>
    <td></td>
    <td>load disabled (+ 2 minutes wait)</td>
  </tr>
</table>

## Case 05: `bad_wifi--no_load--gradual_profile`

Verdict: **problematic** (good when manually configuring --min-latency and --start-latency)

Summary:

* peak jitter: stabilized at 220ms
* target latency: stabilizes at 360ms
* losses: lost 1000ms, several restarts, FEC triggers regularly but can't repair everything

Notes:

* Likely, problems can be fixed by implementing dynamic starting latency.

Sender:

```
roc-send -vv -s rtp+rs8m://raspberrypi-4b-ubuntu.lan:20001 -r rs8m://raspberrypi-4b-ubuntu.lan:20002 \
   -c rtcp://raspberrypi-4b-ubuntu.lan:20004 -i pulse://null.monitor
```

Receiver:

```
roc-recv -vv -s rtp+rs8m://0.0.0.0:20001 -r rs8m://0.0.0.0:20002 -c rtcp://0.0.0.0:20004 \
   -o pulse://default --plc=beep --latency-profile=gradual --dump /tmp/dump.csv
```

Measurements:

[**dump.csv.xz**](05--bad_wifi--no_load--gradual_profile/dump.csv.xz)

<table>
  <tr>
    <td><img width="160px" src="05--bad_wifi--no_load--gradual_profile/screenshot_01.gif"/></td>
    <td><img width="160px" src="05--bad_wifi--no_load--gradual_profile/screenshot_02.gif"/></td>
    <td><img width="160px" src="05--bad_wifi--no_load--gradual_profile/screenshot_03.gif"/></td>
    <td><img width="160px" src="05--bad_wifi--no_load--gradual_profile/screenshot_04.gif"/></td>
    <td><img width="160px" src="05--bad_wifi--no_load--gradual_profile/screenshot_05.gif"/></td>
    <td><img width="160px" src="05--bad_wifi--no_load--gradual_profile/screenshot_06.gif"/></td>
  </tr>
  <tr>
    <td></td>
    <td>restarts</td>
    <td>restarts</td>
    <td>disruptions</td>
    <td></td>
    <td></td>
  </tr>
</table>

## Case 06: `bad_wifi--low_load--gradual_profile`

Verdict: **unusable** (burst delays are too rare and huge - above second)

Summary:

* peak jitter: reached 1100ms
* target latency: reached 2000ms
* losses: many losses and restarts

Notes:

* Not sure if we can do anything here.

Sender:

```
roc-send -vv -s rtp+rs8m://raspberrypi-4b-ubuntu.lan:20001 -r rs8m://raspberrypi-4b-ubuntu.lan:20002 \
   -c rtcp://raspberrypi-4b-ubuntu.lan:20004 -i pulse://null.monitor
```

Receiver:

```
roc-recv -vv -s rtp+rs8m://0.0.0.0:20001 -r rs8m://0.0.0.0:20002 -c rtcp://0.0.0.0:20003 \
    -o pulse://default --plc=beep --latency-profile=gradual \
    --min-latency=1s --max-latency=3s --no-play-timeout=5s \
    --dump /tmp/dump.csv
```

Load (200 pkt/sec):

```
sudo hping3 -i u5000 -S -p 80 raspberrypi-4b-ubuntu.lan
```

Measurements:

[**dump.csv.xz**](06--bad_wifi--low_load--gradual_profile/dump.csv.xz)

<table>
  <tr>
    <td><img width="160px" src="06--bad_wifi--low_load--gradual_profile/screenshot_01.gif"/></td>
    <td><img width="160px" src="06--bad_wifi--low_load--gradual_profile/screenshot_02.gif"/></td>
    <td><img width="160px" src="06--bad_wifi--low_load--gradual_profile/screenshot_03.gif"/></td>
    <td><img width="160px" src="06--bad_wifi--low_load--gradual_profile/screenshot_04.gif"/></td>
    <td><img width="160px" src="06--bad_wifi--low_load--gradual_profile/screenshot_05.gif"/></td>
  </tr>
  <tr>
    <td></td>
    <td></td>
    <td></td>
    <td>load enabled, restarts</td>
    <td>constant restarts</td>
  </tr>
</table>

## Case 07: `ethernet--default_latency--responsive_profile`

Verdict: **good but non-optimal**

Summary:

* peak jitter: very stable at 60-70ms even under very high load
* target latency: stable at 130ms
* losses: none

Notes:

* High jitter is caused by large default frame size, packet size, FEC block, and (likely) PulseAudio. If we implement adaptive FEC, adaptive packet size, and native ALSA backend, this case should be improved.

Sender:

```
roc-send -vv -s rtp+rs8m://raspberrypi-4b-ubuntu.lan:20001 -r rs8m://raspberrypi-4b-ubuntu.lan:20002 \
   -c rtcp://raspberrypi-4b-ubuntu.lan:20004 -i pulse://null.monitor
```

Receiver:

```
roc-recv -vv -s rtp+rs8m://0.0.0.0:20001 -r rs8m://0.0.0.0:20002 -c rtcp://0.0.0.0:20003 \
    -o pulse://default --plc=beep --latency-profile=responsive --dump /tmp/dump.csv
```

Load 1 (1000 pkt/sec):

```
sudo hping3 -i u1000 -S -p 80 raspberrypi-4b-ubuntu.lan
```

Load 2 (10000 pkt/sec):

```
sudo hping3 -i u10 -S -p 80 raspberrypi-4b-ubuntu.lan
```

Measurements:

[**dump.csv.xz**](07--ethernet--default_latency--responsive_profile/dump.csv.xz)

<table>
  <tr>
    <td><img width="160px" src="07--ethernet--default_latency--responsive_profile/screenshot_01.gif"/></td>
    <td><img width="160px" src="07--ethernet--default_latency--responsive_profile/screenshot_02.gif"/></td>
    <td><img width="160px" src="07--ethernet--default_latency--responsive_profile/screenshot_03.gif"/></td>
    <td><img width="160px" src="07--ethernet--default_latency--responsive_profile/screenshot_04.gif"/></td>
  </tr>
  <tr>
    <td></td>
    <td></td>
    <td>load 1 enabled (1000 pkt/sec)</td>
    <td>load 2 enabled (10000 pkt/sec)</td>
  </tr>
</table>

## Case 08: `ethernet--low_latency--responsive_profile`

Verdict: **good**

Summary:

* peak jitter: stable at 12ms
* target latency: started from 50ms, stabilized at 20ms
* losses: none

Notes:

* Likely, remaining jitter is at least partially caused by PulseAudio and can be reduced by implementing native ALSA backend.

Sender:

```
roc-send -vv -s rtp+rs8m://raspberrypi-4b-ubuntu.lan:20001 -r rs8m://raspberrypi-4b-ubuntu.lan:20002 \
    -c rtcp://raspberrypi-4b-ubuntu.lan:20003 -i file:stash/samples/long.wav \
    --packet-len=1ms --frame-len=1ms --nbsrc=10 --nbrpr=7
```

Receiver:

```
roc-recv -vv -s rtp+rs8m://0.0.0.0:20001 -r rs8m://0.0.0.0:20002 -c rtcp://0.0.0.0:20003 \
    -o pulse://default --plc=beep --latency-profile=responsive \
    --start-latency=50ms --io-latency=40ms --frame-len=1ms \
    --dump /tmp/dump.csv
```

Measurements:

[**dump.csv.xz**](08--ethernet--low_latency--responsive_profile/dump.csv.xz)

<table>
  <tr>
    <td><img width="160px" src="08--ethernet--low_latency--responsive_profile/screenshot_01.gif"/></td>
    <td><img width="160px" src="08--ethernet--low_latency--responsive_profile/screenshot_02.gif"/></td>
    <td><img width="160px" src="08--ethernet--low_latency--responsive_profile/screenshot_03.gif"/></td>
    <td><img width="160px" src="08--ethernet--low_latency--responsive_profile/screenshot_04.gif"/></td>
    <td><img width="160px" src="08--ethernet--low_latency--responsive_profile/screenshot_05.gif"/></td>
  </tr>
</table>

## Case 09: `internet--gradual_profile`

Verdict: **mostly good**

Summary:

* peak jitter: stabilized at 90ms, increased to 110ms under medium load, increased to 400ms under high load, returned to 90ms without load
* target latency: started from 200ms, quickly lowered to 160ms, increased to 600ms under load, returned to 200ms without load
* losses: high load caused losses and restarts; FEC is triggered constantly and works; disruptions only in the initial period of high load

Sender:

```
roc-send -vv -s rtp+rs8m://10.9.8.50.lan:20001 -r rs8m://10.9.8.50.lan:20002 \
    -c rtcp://10.9.8.50.lan:20003 -i pulse://null.monitor
```

Receiver:

```
roc-recv -vv -s rtp+rs8m://0.0.0.0:20001 -r rs8m://0.0.0.0:20002 -c rtcp://0.0.0.0:20003 \
    -o pulse://default --plc=beep --latency-profile=gradual --dump /tmp/dump.csv
```

Load 1 (1000 pkt/sec):

```
sudo hping3 -i u1000 -S -p 80 10.9.8.50
```

Load 2 (2000 pkt/sec):

```
sudo hping3 -i u500 -S -p 80 10.9.8.50
```

Measurements:

[**dump.csv.xz**](09--internet--gradual_profile/dump.csv.xz)

<table>
  <tr>
    <td><img width="160px" src="09--internet--gradual_profile/screenshot_01.gif"/></td>
    <td><img width="160px" src="09--internet--gradual_profile/screenshot_02.gif"/></td>
    <td><img width="160px" src="09--internet--gradual_profile/screenshot_03.gif"/></td>
    <td><img width="160px" src="09--internet--gradual_profile/screenshot_04.gif"/></td>
    <td><img width="160px" src="09--internet--gradual_profile/screenshot_05.gif"/></td>
    <td><img width="160px" src="09--internet--gradual_profile/screenshot_06.gif"/></td>
    <td><img width="160px" src="09--internet--gradual_profile/screenshot_07.gif"/></td>
    <td><img width="160px" src="09--internet--gradual_profile/screenshot_08.gif"/></td>
  </tr>
  <tr>
    <td></td>
    <td></td>
    <td></td>
    <td>enable load 1 (1000 pkt/sec)</td>
    <td>enable load 2 (2000 pkt/sec), losses and restarts</td>
    <td></td>
    <td>disable load</td>
    <td></td>
  </tr>
</table>
