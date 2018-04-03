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

insideO = [(ml1[0] + ml2[0]) / 2, (ml1[1] + ml2[1]) / 2, (ml1[2] + ml2[2]) / 2]

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

def putLine(p1, p2, name, div=2):
    global fout
    fout.write('LINE ' + name + ' ' + p1 + ' ' + p2 + ' ' + str(div) + '\n')

def putSurf(l1, l2, l3, l4, name):
    global fout
    fout.write('SURF ' + name + ' ' + ' '.join((l1, l2, l3, l4)) + '\n')

def putBody(s1, s2, name):
    global fout
    fout.write('BODY ! ' + s1 + ' ' + s2 + '\n')

# inner right-side plate
mrbv = basisVec(mr1, mr2, mr3)

p1 = abc(insideO, mrbv[0], 8./12)
p2 = abc(p1, mrbv[1], 7./12)
p3 = abc(p2, mrbv[0], -16./12)
p4 = abc(p3, mrbv[1], -7./12)

p5 = abc(p1, mrbv[2], -.25/12)
p6 = abc(p2, mrbv[2], -.25/12)
p7 = abc(p3, mrbv[2], -.25/12)
p8 = abc(p4, mrbv[2], -.25/12)

putPnt(p1, 'D101')
putPnt(p2, 'D102')
putPnt(p3, 'D103')
putPnt(p4, 'D104')

putPnt(p5, 'D105')
putPnt(p6, 'D106')
putPnt(p7, 'D107')
putPnt(p8, 'D108')

putLine('D101', 'D102', 'L101', 4)
putLine('D102', 'D103', 'L102', 4)
putLine('D103', 'D104', 'L103', 4)
putLine('D104', 'D101', 'L104', 4)

putLine('D105', 'D106', 'L105', 4)
putLine('D106', 'D107', 'L106', 4)
putLine('D107', 'D108', 'L107', 4)
putLine('D108', 'D105', 'L108', 4)

# inner left-side plate
mlbv = basisVec(ml1, ml2, ml3)

p1 = abc(insideO, mlbv[0], 8./12)
p2 = abc(p1, mlbv[1], 7./12)
p3 = abc(p2, mlbv[0], -16./12)
p4 = abc(p3, mlbv[1], -7./12)

p5 = abc(p1, mlbv[2], .25/12)
p6 = abc(p2, mlbv[2], .25/12)
p7 = abc(p3, mlbv[2], .25/12)
p8 = abc(p4, mlbv[2], .25/12)

putPnt(p1, 'D201')
putPnt(p2, 'D202')
putPnt(p3, 'D203')
putPnt(p4, 'D204')

putPnt(p5, 'D205')
putPnt(p6, 'D206')
putPnt(p7, 'D207')
putPnt(p8, 'D208')

putLine('D201', 'D202', 'L201', 4)
putLine('D202', 'D203', 'L202', 4)
putLine('D203', 'D204', 'L203', 4)
putLine('D204', 'D201', 'L204', 4)

putLine('D205', 'D206', 'L205', 4)
putLine('D206', 'D207', 'L206', 4)
putLine('D207', 'D208', 'L207', 4)
putLine('D208', 'D205', 'L208', 4)

fout.write('INT L105 L205\n')
fout.write('INT L107 L207\n')

putLine('D101', 'D105', 'L109')
putLine('D102', 'D106', 'L110')
putLine('D103', 'D107', 'L111')
putLine('D104', 'D108', 'L112')

putSurf('L101', 'L102', 'L103', 'L104', 'S101')
putSurf('L105', 'L106', 'L107', 'L108', 'S102')

putBody('S101', 'S102', 'B101')

putLine('D201', 'D205', 'L209')
putLine('D202', 'D206', 'L210')
putLine('D203', 'D207', 'L211')
putLine('D204', 'D208', 'L212')

putSurf('L201', 'L202', 'L203', 'L204', 'S201')
putSurf('L205', 'L206', 'L207', 'L208', 'S202')

putBody('S201', 'S202', 'B201')

fout.write('ELTY all he20r\n')
