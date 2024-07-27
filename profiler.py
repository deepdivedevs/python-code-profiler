import time
import tracemalloc
import typing
import matplotlib.pyplot as plt
import pandas as pd


class Profiler:
    def __init__(self):
        self.function_stats = {}

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            start = time.time()
            tracemalloc.start()
            start_memory = tracemalloc.get_traced_memory()[0]
            
            # Call the original function and save the return result
            result = func(*args, **kwargs)
            end = time.time()
            end_memory = tracemalloc.get_traced_memory()[0]
            tracemalloc.stop()

            execution_time = end - start
            memory_used = end_memory - start_memory 

            if func.__name__ not in self.function_stats:
                self.function_stats[func.__name__] = {"calls": 0, "total_time": 0, "total_memory": 0}
            self.function_stats[func.__name__]["calls"] += 1
            self.function_stats[func.__name__]["total_time"] += execution_time
            self.function_stats[func.__name__]["total_memory"] += memory_used

            # Return the result of func(), so when we execute the wrapper function we have the result
            return result
        return wrapper

    def print_stats(self, sort_by='total_time', reverse=True, filter_function=None, top_n=None):
            stats = self.get_stats()
    
            if filter_function:
                stats = list(filter(filter_function, stats))
    
            stats.sort(key=lambda x: x[sort_by], reverse=reverse)
    
            if top_n:
                stats = stats[:top_n]
    
            print(f"{'Function':<20} {'Calls':<10} {'Total Time':<15} {'Avg Time':<15} {'Total Memory':<20} {'Avg Memory':<20}")
            print("-" * 100)
            for stat in stats:
                print(f"{stat['name']:<20} {stat['calls']:<10} {stat['total_time']:.6f}s      {stat['avg_time']:.6f}s      {stat['total_memory']:,} bytes      {stat['avg_memory']:,.0f} bytes")

    def get_stats(self):
        stats = []
        for func_name, data in self.function_stats.items():
            calls = data['calls']
            total_time = data['total_time']
            total_memory = data['total_memory']
            avg_time = total_time / calls
            avg_memory = total_memory / calls
            stats.append({
                'name': func_name,
                'calls': calls,
                'total_time': total_time,
                'avg_time': avg_time,
                'total_memory': total_memory,
                'avg_memory': avg_memory
            })
        return stats
        
    
    def visualize(self, metric='total_time', top_n=10):
        stats = self.get_stats()
        stats.sort(key=lambda x: x[metric], reverse=True)
        stats = stats[:top_n]

        functions = [stat['name'] for stat in stats]
        values = [stat[metric] for stat in stats]

        plt.figure(figsize=(12,6))
        plt.bar(functions, values)
        plt.title(f'Top {top_n} Functions by {metric.replace("_", " ").title()}')
        plt.xlabel('Functions')
        plt.ylabel(metric.replace('_', ' ').title())
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()

    def export(self, filename=f"{datetime.today().strftime('%Y-%m-%d %H:%M:%S')}-profile.csv"):
        pd.DataFrame.from_dict(profiler.function_stats, orient='index').to_csv(filename)