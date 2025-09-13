# Python Garbage Collection

Garbage collection in Python does not work the way you think, at least it did not for me.

This repository explores different aspects of garbage collection and aims to give an insight what is going on.

Just follow the steps mentioned here.

## Dependencies

We will profile meory of an example application, thus the `memory_profiler` package is needed. Install it via

```shell
$ pip install memory_profiler
```

Also install `numpy` and `matplotlib` the same way.

## General execution instruction

To generate the profile for a file, run `mprof run {name of the file}.py`. A `mprof_*.dat` file will be generated with the
time series of memory used. In order to plot it, use `mprof plot`. Should you receive a warning, it might be because
you are not in an interactive mode. Then use `mprof plot --out {name of output file}.png`.

## About the program

The code in question creates multiple "large" arrays of random integers and computes the average over all numbers. The 
functions wait before returning the result so that the impact on memory is easier to see on the graph.

## Establishing baseline

Run the file `baseline.py` as mentioned under [above](#general_execution_instruction)

You should see a graph with 3 bumps. The beginning and end of every function call should be indicated by brackets.

At the beginning of every function memory usage increases when the array is generated, then stays constant during the 
period it sleeps and in the end goes done again when the function is left and temporary variables are cleaned up.

Note how the decrease in memory is still within the brackets of a function call, indicating that the clean up of memory
is considered to be part of the function.

## Introducing gc

The whole point of this repository is the package [gc](https://docs.python.org/3/library/gc.html) which provides and 
interface to the garbage collector of Python. It especially enables us to disable garbage collection.

Applied to the situation above, this would mean that we no longer see a decrease in memory usage on the graph. It would
only continually rise.

Check out `gc.py`. There, garbage collection is disabled before the arrays are being created.

Profile the code and checkout the graph.

## What is going on?

You should see a picture that is similar to the first one. Maybe the graph looks slightly different and memory usage levels
are not the same. This can be due to the timing of the measurements or because memory profiling is not fully deterministic.

Also note how - apparently - the `gc` package is messing with the brackets in the graph. No idea what is going on here.

But we do not see the continual increase of memory. Why is that? To answer that question, we take a closer look at garbage
collection.

## Garbage collection in Python

There are two mechanisms at play when it comes to garbage collection in Python:
* Reference counting
* Circular references

The first one checks how many references to a piece of memory exists and if this count goes to zero, the memory is freed.
This is what is happening in our example. Once a function is left, all temporary variables are deleted and thus the 
underlying memory is freed.

But there is a situation when this is not possible, that is in the case of circular references, e.g. when an object
holds a reference to itself or when an object has the reference to another object which has a reference to the first one.

These cases cannot be freed through reference counting and thus a dedicated garbage collector exists for it and this 
second garbage collector is controlled via the `gc` package.

## Garbage collection disabled

Check out `gc_cr.py`. There we create a list that contains our array and also a 
reference to itself. This is enough to persist the memory allocation even after the function was left.

Run the code and check out the graph.

Here is the picture we wanted to see. The memory usage is constantly increasing. Garbage collection is disabled. So we
are done, right?

Well, maybe not! Because the real surprise comes now.

Run `cr_only.py` where garbage collection is *not* disabled.

We see the same plot - now with brackets again. This means that the circular references are not removed even though
garbage collection is on. This implies that the second garbage collector is not constantly running.

## Manual garbage collection

Let's try the opposite from before. We will manually trigger garbage collection and check whether we see it on the 
memory profile.

Run `manual_gc_cr.py` where a manual collection is triggered before the third time
the array is created.

You should see and increase in memory from the first to the second run but then a retraction back to the level before
the first run.
Also, the runtime of the collection run should be printed. For me, it roughly took 5 milliseconds. I cannot say for sure
whether that is expensive compared to the other garbage collector and thus not done constantly.
