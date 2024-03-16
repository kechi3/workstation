import numpy as np

u_rod = 2
d_rod = 2
contact = 40
n_elm = u_rod+d_rod+contact+1
node = n_elm + 1

r_u_rod = 0.1
r_d_rod = 0.7
r_contact = 2.65-r_u_rod-r_d_rod
r_target = 1

q_u_rod = 1.
q_d_rod = 7.
q_contact = 25.6

R = np.zeros(n_elm)
q = np.zeros(node)
t = np.zeros(node)
t[0] = 20
t[node-1] = 20

dum = 0
for i in range(d_rod):
    R[dum] = r_d_rod/d_rod
    if i > 0 and i < d_rod:
        q[dum] = q_d_rod/(d_rod-1)
    dum += 1
for i in range(contact+1):
    R[dum] = r_contact/contact
    if i > 0 and i < contact+1:
        q[dum] = 25.6/contact
    dum += 1
R[dum-int(contact/2+1)] = r_target
for i in range(u_rod):
    R[dum] = r_u_rod/u_rod
    if i > 0 and i < u_rod:
        q[dum] = q_u_rod/(u_rod-1)
    dum += 1

"""
print(R)
print(q)
print(t)
"""

A = np.zeros((node,node))

for i in range(n_elm):
   A[i,i] += 1/R[i] 
   A[i+1,i+1] += 1/R[i] 
   A[i,i+1] -= 1/R[i] 
   A[i+1,i] -= 1/R[i] 

for i in range(node):
    if t[i] > 0.:
        A[i] = 0.
        A[i,i] = 1.
        q[i] = t[i]

t = np.linalg.solve(A, q)

print(t)






