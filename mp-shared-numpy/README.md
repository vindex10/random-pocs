Share same numpy array among several subprocesses. For instance when acquiring a bunch of data is costly, but one
has to process it in various ways.


As a test, just check your RAM usage for two alternative cases:

* With shared memory:

```
python3 multi.py
```


* Without shared memory:

```
python3 multi.py --no-share
```
