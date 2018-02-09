#!/usr/bin/python

import math

fout = open('model.inp', 'w')

height = 16 #feet
rings = 9
el_per_ring = 8
r_del = 2 * math.pi / el_per_ring

nodes = []
elements = []

r1 = 4./3
r2 = 2
r3 = 4.5
r_mid = 6

def trunk_rad(i):
    if i < 5:
        return r2
    else:
        return r1

# horizontal trunk segments
for i in range(rings):

    z = i * float(height) / rings
    # this is a logistic function for smooth tapering
    #r = r1 + (r2 - r1) / (1 + math.exp((12./rings) * i - 6))
    # this is a step function for easy construction
    r = trunk_rad(i)

    for j in range(el_per_ring):

        r_this = j * r_del
        if i % 2 == 0:
            r_this += r_del / 2

        r_next = r_this + r_del

        x = r * math.cos(r_this)
        y = r * math.sin(r_this)

        x_next = r * math.cos(r_next)
        y_next = r * math.sin(r_next)

        x2 = (x + x_next) / 2
        y2 = (y + y_next) / 2

        nodes.append([x, y, z])
        nodes.append([x2, y2, z])

        n1 = len(nodes) - 2
        n2 = n1 + 1
        if j == el_per_ring - 1:
            n3 = i * el_per_ring * 2
        else:
            n3 = n2 + 1
        elements.append([n1, n2, n3])

# diagonal trunk segments
for i in range(rings - 1):

    for j in range(el_per_ring):

        n1 = (i * el_per_ring + j) * 2
        n2 = n1 + el_per_ring * 2
        if i % 2 == 1:
            n2 -= 2
        n3 = n2 + 2

        n2 = (i + 1) * el_per_ring * 2 + (n2 % (el_per_ring * 2))
        n3 = (i + 1) * el_per_ring * 2 + (n3 % (el_per_ring * 2))

        x1 = (nodes[n1][0] + nodes[n2][0]) / 2
        y1 = (nodes[n1][1] + nodes[n2][1]) / 2
        z1 = (nodes[n1][2] + nodes[n2][2]) / 2

        x2 = (nodes[n1][0] + nodes[n3][0]) / 2
        y2 = (nodes[n1][1] + nodes[n3][1]) / 2
        z2 = (nodes[n1][2] + nodes[n3][2]) / 2

        nodes.append([x1, y1, z1])
        nodes.append([x2, y2, z2])

        elements.append([n1, len(nodes) - 2, n2])
        elements.append([n1, len(nodes) - 1, n3])

# roots
for n in [33, 37, 41, 45]:
    r2dl = math.sqrt(nodes[n-1][0] ** 2 + nodes[n-1][1] ** 2) # root 2D length
    r2dn = [nodes[n-1][0] / r2dl * r_mid, nodes[n-1][1] / r2dl * r_mid, 0] # root 2D end node
    rm = [(nodes[n-1][0] + r2dn[0]) / 2, (nodes[n-1][1] + r2dn[1]) / 2, (nodes[n-1][2] + r2dn[2]) / 2] # root midpoint
    nodes.append(rm)
    nodes.append(r2dn)
    elements.append([n-1, len(nodes) - 2, len(nodes) - 1])

# midgard
z_mid = nodes[68][2]
for n in [69, 71, 73, 75]:
    mn = [-r_mid, nodes[n-1][1], z_mid]
    mm = [(nodes[n-1][0] - r_mid) / 2, nodes[n-1][1], z_mid]
    nodes.append(mm)
    nodes.append(mn)
    elements.append([n-1, len(nodes) - 2, len(nodes) - 1])
for i in [(282, 284), (284, 286), (286, 288)]:
    x_mid = (nodes[i[0]-1][0] + nodes[i[1]-1][0]) / 2
    y_mid = (nodes[i[0]-1][1] + nodes[i[1]-1][1]) / 2
    z_mid = (nodes[i[0]-1][2] + nodes[i[1]-1][2]) / 2
    s_mid = [x_mid, y_mid, z_mid]
    nodes.append(s_mid)
    elements.append([i[0]-1, len(nodes) - 1, i[1]-1])

# midgard supports
for i in [(281, 55), (283, 55), (283, 57), (285, 57), (285, 59), (287, 59)]:#, (282, 37), (284, 39), (286, 41), (288, 43)]:
    x_mid = (nodes[i[0]-1][0] + nodes[i[1]-1][0]) / 2
    y_mid = (nodes[i[0]-1][1] + nodes[i[1]-1][1]) / 2
    z_mid = (nodes[i[0]-1][2] + nodes[i[1]-1][2]) / 2
    s_mid = [x_mid, y_mid, z_mid]
    nodes.append(s_mid)
    elements.append([i[0]-1, len(nodes) - 1, i[1]-1])

fout.write('*NODE,NSET=Nall\n')
for i, node in enumerate(nodes):

    node_line = str(i + 1) + ', ' + str(node[0]) + ', ' + str(node[1]) + ', ' + str(node[2]) + '\n'

    fout.write(node_line)

fout.write('*ELEMENT,TYPE=B32,ELSET=EAll\n')
for i, el in enumerate(elements):

    el_line = str(i + 1) + ', ' + str(el[0] + 1) + ', ' + str(el[1] + 1) + ', ' + str(el[2] + 1) + '\n'

    fout.write(el_line)

fout.write('*BOUNDARY\n')
for i in [1,3,5,7,9,11,13,15,274,276,278,280]:
    fout.write(str(i) + ',1,3\n')

fout.write('*MATERIAL,NAME=WOOD\n')
fout.write('*ELASTIC\n')
fout.write('2.5E8,.038\n')

fout.write('*BEAM SECTION,ELSET=EAll,MATERIAL=WOOD,SECTION=RECT\n')
fout.write('.125,.292\n')

fout.write('*STEP\n')
fout.write('*STATIC\n')
fout.write('*CLOAD\n')
fout.write('282,3,-1.\n')
fout.write('284,3,-1.\n')
fout.write('286,3,-1.\n')
fout.write('288,3,-1.\n')

fout.write('*EL PRINT,ELSET=Eall\n')
fout.write('S\n')

fout.write('*EL FILE\n')
fout.write('S\n')

fout.write('*NODE FILE\n')
fout.write('U\n')

fout.write('*END STEP\n')
