# What is sohot

Simply speaking, sohot is a local area network timely communication tool, because it is based on Python's asyncio, UDP, celery implementation, so it seems more attractive.

## How to

* sohot --help

### How to start

* setp 1
```
$ 1.start_celery_queue.sh
```
* step 2
```
$ 2.start_echoserver.sh
```
* step 3
```
$ 3.start_client_console.sh
```
### How to stop

* step 1
```
$ stop_1_celery_queue.sh
```
* step 2
```
$ stop_2_sohot.sh
```