### octave/matlab
```matlab
1;
function P=solve(M)
  if M<2 
    P=0.0;
    return;
  end
  if M>365 
    P=1.0;
    return;
  end
  P=1.0-prod(1.0-(0:(M-1))/365);
end

M=sscanf(fgetl(stdin),"%d");
fprintf(stdout,"%.9f\n",solve(M));
```

### julia
```julia
function solve(M)
  M>365 && return 1.0
  M<2 && return 0.0
  1.0 - prod(1 .- (0:(M-1)) / 365)
end

M=parse(Int,readline())
println(solve(M))
```

### python
```python
import numpy as np
def solve(M):
  if M<2:
    return 0
  if M>365:
    return 1
  return 1.0-np.prod(1.0 - np.array(range(0,M))/365.0)

M=int(input())
print(solve(M))
```