#!/usr/bin/python

import math

fout = open('conn1.fbd', 'w')


 # top left
tl1 = [-3.058873475755e+00, 2.438629796090e-02, 2.062150895304e+00] # D010
tl2 = [-3.011288243174e+00, 2.635806199595e-01, 1.901571562993e+00] # D011
tl3 = [-2.856730000000e+00, 1.040650000000e+00, 3.635850000000e+00] # D00I

 # top right
tr1 = [-3.058873475755e+00, -2.438629796090e-02, 2.062150895304e+00] # D015
tr2 = [-3.011288243181e+00, -2.635806199589e-01, 1.901571562995e+00] # D016
tr3 = [-2.856730000000e+00, -1.040650000000e+00, 3.635850000000e+00] # D00T

 # bottom left
bl1 = [-3.011288243174e+00, 2.635806199595e-01, 1.653988437007e+00] # D00M
bl2 = [-3.058873475755e+00, 2.438629796090e-02, 1.493409104696e+00] # D00L
bl3 = [-2.856730000000e+00, 1.040650000000e+00, -8.028950000000e-02] # D003

 # bottom right
br1 = [-3.058873475755e+00, -2.438629796090e-02, 1.493409104696e+00] # D00Q
br2 = [-3.011288243181e+00, -2.635806199589e-01, 1.653988437005e+00] # D00R
br3 = [-2.856730000000e+00, -1.040650000000e+00, -8.028950000000e-02] # D007

 # middle left
ml1 = [-2.932352948060e+00, 0.000000000000e+00, 1.923780000000e+00] # D01G
ml2 = [-2.932352948060e+00, 0.000000000000e+00, 1.631780000000e+00] # D01H
ml3 = [-2.063580000000e+00, 2.097400000000e+00, 1.923780000000e+00] # D01B

 # middle right
mr1 = [-2.932352948060e+00, 0.000000000000e+00, 1.923780000000e+00] # D01G
mr2 = [-2.932352948060e+00, 0.000000000000e+00, 1.631780000000e+00] # D01H
mr3 = [-2.063580000000e+00, -2.097400000000e+00, 1.923780000000e+00] # D018

o = [(ml1[0] + ml2[0]) / 2, (ml1[1] + ml2[1]) / 2, (ml1[2] + ml2[2]) / 2]

def cent(p):
    global ml1, ml2

    a = [(ml1[0] + ml2[0]) / 2, (ml1[1] + ml2[1]) / 2, (ml1[2] + ml2[2]) / 2]

    return [p[0] - a[0], p[1] - a[1], p[2] - a[2]]

def uncent(p):
    pass

def dotProd(v1, v2):
    return v1[0]*v2[0] + v1[1]*v2[1] + v1[2]*v2[2]

def crossProd(v1, v2):
    return [v1[1]*v2[2] - v1[2]*v2[1], v1[2]*v2[0] - v1[0]*v2[2], v1[0]*v2[1] - v1[1]*v2[0]]

def vecLen(v):
    return math.sqrt(v[0]*v[0] + v[1]*v[1] + v[2]*v[2])

def basisVec(p1, p2, p3):
    a = [p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2]]
    b = [p3[0] - p1[0], p3[1] - p1[1], p3[2] - p1[2]]

    c = crossProd(a, b)
    lenC = vecLen(c)
    norm = [c[0] / lenC, c[1] / lenC, c[2] / lenC]

    up = [0, 0, 1]

    upDotNorm = dotProd(up, norm)
    upDotNormTNorm = [norm[0] * upDotNorm, norm[1] * upDotNorm, norm[2] * upDotNorm]

    upProj = [up[0] - upDotNormTNorm[0], up[1] - upDotNormTNorm[1], up[2] - upDotNormTNorm[2]]
    lenUpProj = vecLen(upProj)
    v1 = [upProj[0] / lenUpProj, upProj[1] / lenUpProj, upProj[2] / lenUpProj]

    v2 = crossProd(v1, norm)

    return [v1, v2, norm]

def abc(p1, p2, c):
    return [p1[0] + p2[0]*c, p1[1] + p2[1]*c, p1[2] + p2[2]*c]

def putPnt(p, name):
    global fout
    fout.write('PNT ' + name + ' ' + str(p[0]) + ' ' + str(p[1]) + ' ' + str(p[2]) + '\n')

def putLine(p1, p2):
    global fout
    fout.write('LINE ! ' + p1 + ' ' + p2 + ' 2\n')

mrbv = basisVec(mr1, mr2, mr3)
bv1 = mrbv[0]
bv2 = mrbv[1]

p1 = abc(o, bv1, 0.5)
p2 = abc(p1, bv2, 0.6)
p3 = abc(p2, bv1, -1.0)
p4 = abc(p3, bv2, -0.6)

putPnt(p1, 'D101')
putPnt(p2, 'D102')
putPnt(p3, 'D103')
putPnt(p4, 'D104')

putLine('D101', 'D102')
putLine('D102', 'D103')
putLine('D103', 'D104')
putLine('D104', 'D101')
