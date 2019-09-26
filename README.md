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
# flow
```flow
st=>start: 注册印象笔记
e=>end: 您可以使用markdown
op1=>operation: 登录印象笔记
op2=>operation: 购买并登录马克飞象
cond=>condition: 是否已经购买并登录了马克飞象?

st->op1->cond
cond(yes)->e
cond(no)->op2->e

```
