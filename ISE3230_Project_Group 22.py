#!/usr/bin/env python
# coding: utf-8

# In[4]:


import cvxpy as cp

# Binary decision variables for weeks 1-5 indicating departing city with rows and entering city with column
x1 = cp.Variable((14,14), boolean = True)
x2 = cp.Variable((14,14), boolean = True)
x3 = cp.Variable((14,14), boolean = True)
x4 = cp.Variable((14,14), boolean = True)
x5 = cp.Variable((14,14), boolean = True)

x = [x1,x2,x3,x4,x5]

# Distance in Km (row is start, column is destination)
d = [[0,516.8325,259.3497,1090.3737,472.0779,79.3667,649.1763,446.5609,334.2242,415.6559,820.4459,799.0255,680.1633,326.1386], #Michigan
     [516.8325,0,446.8176,1584.9493,988.4668,590.0207,1149.1204,882.2584,766.5048,760.9393,1333.7649,288.2574,217.0555,832.141], #Penn State
     [259.3497,446.8176,0,1162.4109,632.5238,327.2505,741.5638,444.5599,334.8576,314.2923,1003.0054,728.6889,533.5022,454.5827], #Ohio State
     [1090.3737,1584.9493,1162.4109,0,653.4124,1035.5588,441.3441,721.5636,827.5794,886.5361,542.6726,1873.1876,1695.8177,764.402], #Nebraska
     [472.0779,988.4668,632.5238,653.4124,0,403.5935,235.8584,344.8891,359.1107,495.9406,371.61,1270.9528,1139.5307,179.9801], #Wisconsin
     [79.3667,590.0207,327.2505,1035.5588,403.5935,0,594.6662,428.5279,325.9551,430.5023,744.4239,868.8807,758.3315,273.8011], #Michigan
     [649.1763,1149.1204,741.5638,441.3441,235.8584,594.6662,0,328.5887,412.0731,507.2955,393.4202,1436.8982,1272.7872,323.0952], #Iowa
     [446.5609,882.2584,444.5599,721.5636,344.8891,428.5279,328.5887,0,117.9596,178.7405,679.5567,1168.7596,976.1724,223.5637], #Illinois
     [334.2242,766.5048,334.8576,827.5794,359.1107,325.9551,412.0731,117.9596,0,143.5175,721.9126,1053.7266,868.3444,192.7782], #Purdue
     [415.6559,760.9393,314.2923,886.5361,495.9406,430.5023,507.2955,178.7405,143.5175,0,849.436,1040.5434,827.5057,335.8864], #Indiana
     [820.4459,1333.7649,1003.0054,542.6726,371.61,744.4239,393.4202,679.5567,721.9126,849.436,0,1607.7295,1498.9802,551.5373], #Minnesota
     [799.0255,288.2574,728.6889,1873.1876,1270.9528,868.8807,1436.8982,1168.7596,1053.7266,1040.5434,1607.7295,0,271.7508,1118.6235], #Rutgers
     [680.1633,217.0555,533.5022,1695.8177,1139.5307,758.3315,1272.7872,976.1724,868.3444,827.5057,1498.9802,271.7508,0,970.5945], #Maryland
     [326.1386,832.141,454.5827,764.402,179.9801,273.8011,323.0952,223.5637,192.7782,335.8864,551.5373,1118.6235,970.5945,0]] #Northwestern

# Home or Away (row is what school, columns represent weeks 1-5)
HOrA = [[1, 1, 1, 0, 0], 
       [1, 1, 1, 1, 0], 
       [1, 1, 1, 1, 0],
       [1, 1, 0, 1, 0],
       [1, 1, 1, 0, 1],
       [1, 1, 1, 0, 0],
       [1, 1, 0, 1, 0], 
       [1, 0, 1, 1, 0], 
       [1, 0, 1, 0, 1],
       [1, 1, 0, 0, 1],
       [0, 0, 1, 1, 1],
       [0, 1, 0, 1, 1],
       [1, 0, 1, 1, 1], 
       [1, 0, 1, 0, 0]]

constraints = []

# First row is the school we depart from
constraints.append(cp.sum(x1[0,:]) == 1)

# Do not allow traveling to the same place you start from
for matrix in x:
    constraints.append(cp.trace(matrix) == 0)

# Only one selection per x matrix  
constraints.append(cp.sum(x1) == 1)
constraints.append(cp.sum(x2) == 1)
constraints.append(cp.sum(x3) == 1)
constraints.append(cp.sum(x4) == 1)
constraints.append(cp.sum(x5) == 1)

# Don't go back to anywhere you've gone already
constraints.append(sum(x1[0,i] for i in range(14)) + sum(x1[i,0] for i in range(14)) + sum(x2[0,i] for i in range(14)) + sum(x2[i,0] for i in range(14)) + sum(x3[0,i] for i in range(14)) + sum(x3[i,0] for i in range(14)) + sum(x4[0,i] for i in range(14)) + sum(x4[i,0] for i in range(14)) + sum(x5[0,i] for i in range(14)) + sum(x5[i,0] for i in range(14)) == 1)

for j in range(1,14) :
    constraints.append(sum(x1[j,i] for i in range(14)) + sum(x1[i,j] for i in range(14)) + sum(x2[j,i] for i in range(14)) + sum(x2[i,j] for i in range(14)) + sum(x3[j,i] for i in range(14)) + sum(x3[i,j] for i in range(14)) + sum(x4[j,i] for i in range(14)) + sum(x4[i,j] for i in range(14)) + sum(x5[j,i] for i in range(14)) + sum(x5[i,j] for i in range(14)) <= 2)

# Make sure you leave from where you arrived in the previous step
for j in range(14) :
    constraints.append(sum(x1[i,j] for i in range(14)) == sum(x2[j,i] for i in range(14)))
    constraints.append(sum(x2[i,j] for i in range(14)) == sum(x3[j,i] for i in range(14)))
    constraints.append(sum(x3[i,j] for i in range(14)) == sum(x4[j,i] for i in range(14)))
    constraints.append(sum(x4[i,j] for i in range(14)) == sum(x5[j,i] for i in range(14)))

# Close nodes with away games
for i in range(14):
    if(HOrA[i][0] == 0):
        constraints.append(x1[:,i] == 0)
for i in range(14):
    if(HOrA[i][1] == 0):
        constraints.append(x2[:,i] == 0)
for i in range(14):
    if(HOrA[i][2] == 0):
        constraints.append(x3[:,i] == 0)
for i in range(14) :
    if(HOrA[i][3] == 0):
        constraints.append(x4[:,i] == 0)
for i in range(14):
    if(HOrA[i][4] == 0):
        constraints.append(x5[:,i] == 0)

# Objective Function: Minimizes total distance traveled in kilometers between 6 Big 10 games starting at Michigan
obj_func = cp.sum([cp.sum(d[i][j]*x1[i,j] + d[i][j]*x2[i,j]+ d[i][j]*x3[i,j]+ d[i][j]*x4[i,j]+ d[i][j]*x5[i,j]) for i in range(14) for j in range(14)])

problem=cp.Problem(cp.Minimize(obj_func), constraints)
problem.solve(solver=cp.GUROBI, verbose = True, qcp = True)

print("obj_func =")
print(obj_func.value)
print("x =")
for matrix in x:
    print(matrix.value)


# In[ ]:




