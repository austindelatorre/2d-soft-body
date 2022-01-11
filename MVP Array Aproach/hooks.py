from numba import jit
import time
@jit(nopython=True)
def hookes_law(x1, y1, x2, y2, d, k, damp):
	
	fro i in range(1000)


start = time.time()
f_p(0,5,0,0,6,10,0)
end = time.time()
print("Elapsed (normal) = %s" % (end - start))


# DO NOT REPORT THIS... COMPILATION TIME IS INCLUDED IN THE EXECUTION TIME!
start = time.time()
f(0,5,0,0,6,10,0)
end = time.time()
print("Elapsed (with compilation) = %s" % (end - start))

# NOW THE FUNCTION IS COMPILED, RE-TIME IT EXECUTING FROM CACHE
start = time.time()
f(0,5,0,0,6,10,0)
end = time.time()
print("Elapsed (after compilation) = %s" % (end - start))