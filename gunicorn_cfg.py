import multiprocessing

workers=multiprocessing.cpu_count()
worker_class='gevent'
threads=multiprocessing.cpu_count()*2
worker_connections=100
keepalive=60

