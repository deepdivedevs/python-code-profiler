# python-code-profiler
Simple code profiler using a decorator

Watch the associated Youtube video [here](https://www.youtube.com/watch?v=iDVBwa2C7Us)

## Usage
### Instantiation
Instantiate the Profiler:
```
profiler = Profiler()
```

Then add `@profiler` as a decorator to any function:
```
@profiler
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True
```

Run the function, for example:
```
import random

N = 10000

for i in range(N):
    num = random.randint(2, 100000)
    is_prime(num)
```
### Features

**Print Statistics**
<br>
`Profiler.print_stats(sort_by='total_time', reverse=True, filter_function=None, top_n=None)`
 - `sort_by`: Sort metrics by a specific metric
 - `reverse`: Reverse order of sorting
 - `filter_function`: Filter function to be applied to the stats
 - `top_n`: Only display `top_n` functions

```
> profiler.print_stats()

Function             Calls      Total Time      Avg Time        Total Memory         Avg Memory          
----------------------------------------------------------------------------------------------------
is_prime             10000      0.045105s      0.000005s      7,194 bytes      1 bytes
```

**Visualize Statistics**
<br>
`Profiler.visualize(metric='total_time', top_n=10)`
- `metric`: Metric to visualize on the graph
- `top_n`: Only display `top_n` functions

**Export as CSV**
<br>
`Profiler.export(filename)`
- `filename`: Filename to write out to (default is: `Y-m-d H:M:S-profile.csv`)
  



