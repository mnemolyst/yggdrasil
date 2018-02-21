#!/usr/bin/python

import math

fout = open('model.inp', 'w')

height = 16 #feet
rings = 9
el_per_ring = 8
r_del = 2 * math.pi / el_per_ring

nodes = []
elements = {
        '2x4': [],
        '2x10': [],
        '4x4': [],
        'acry': [],
        }

r_top = 2
r_bot = 3
r_asg = 6
r_mid = 8

def trunk_rad(i):
    if i < 5:
        return r_bot
    else:
        return r_top

# horizontal trunk segments
for i in range(rings):

    z = i * float(height) / rings
    # this is a logistic function for smooth tapering
    #r = r_top + (r_bot - r_top) / (1 + math.exp((12./rings) * i - 6))
    # this is a step function for easy construction
    r = trunk_rad(i)

    for j in range(el_per_ring):

        r_this = j * r_del - ((i + 1) * r_del / 2)

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
        elements['2x4'].append([n1, n2, n3])

# diagonal trunk segments
for i in range(rings - 1):
    j1 = i * el_per_ring * 2
    j2 = (i + 1) * el_per_ring * 2

    for j in range(el_per_ring + el_per_ring):

        # these elements are cut in thirds to brace bifrost
        if (j1+1, j2+1) in [ \
                (75, 93), (75, 91), (73, 91), \
                (67, 85), (67, 83), (65, 83), \
                (89, 107), (89, 105), (87, 105), \
                (81, 99), (81, 97), (95, 97), \
                (103, 121), (103, 119), (101, 119), \
                (111, 113), (111, 127), (109, 127)]:
            for k in range(1, 6):
                mx = nodes[j1][0] + (nodes[j2][0] - nodes[j1][0]) / 6 * k
                my = nodes[j1][1] + (nodes[j2][1] - nodes[j1][1]) / 6 * k
                mz = nodes[j1][2] + (nodes[j2][2] - nodes[j1][2]) / 6 * k

                nodes.append([mx, my, mz])

            l = len(nodes)
            elements['2x4'].append([j1, l-5, l-4])
            elements['2x4'].append([l-4, l-3, l-2])
            elements['2x4'].append([l-2, l-1, j2])
        else:
            mx = nodes[j1][0] + (nodes[j2][0] - nodes[j1][0]) / 2
            my = nodes[j1][1] + (nodes[j2][1] - nodes[j1][1]) / 2
            mz = nodes[j1][2] + (nodes[j2][2] - nodes[j1][2]) / 2

            nodes.append([mx, my, mz])

            elements['2x4'].append([j1, len(nodes) - 1, j2])

        if j%2 == 0:
            j2 = (i + 1) * el_per_ring * 2 + ((j2 + 2) % (el_per_ring * 2))
        else:
            j1 = i * el_per_ring * 2 + ((j1 + 2) % (el_per_ring * 2))

# roots
for n in [33, 37, 41, 45]:
    r2dl = math.sqrt(nodes[n-1][0] ** 2 + nodes[n-1][1] ** 2) # root 2D length
    r2dn = [nodes[n-1][0] / r2dl * r_mid, nodes[n-1][1] / r2dl * r_mid, 0] # root 2D end node
    rm = [(nodes[n-1][0] + r2dn[0]) / 2, (nodes[n-1][1] + r2dn[1]) / 2, (nodes[n-1][2] + r2dn[2]) / 2] # root midpoint
    nodes.append(rm)
    nodes.append(r2dn)
    elements['4x4'].append([n-1, len(nodes) - 2, len(nodes) - 1])

# midgard
z_mid = nodes[68][2]
for n in [75, 77, 79, 65]:
    mn = [-r_mid, nodes[n-1][1], z_mid]
    mm = [(nodes[n-1][0] - r_mid) / 2, nodes[n-1][1], z_mid]
    nodes.append(mm)
    nodes.append(mn)
    elements['2x4'].append([n-1, len(nodes) - 2, len(nodes) - 1])
for i in [(354, 356), (356, 358), (358, 360)]:
    mx = (nodes[i[0]-1][0] + nodes[i[1]-1][0]) / 2
    my = (nodes[i[0]-1][1] + nodes[i[1]-1][1]) / 2
    mz = (nodes[i[0]-1][2] + nodes[i[1]-1][2]) / 2
    s_mid = [mx, my, mz]
    nodes.append(s_mid)
    elements['2x4'].append([i[0]-1, len(nodes) - 1, i[1]-1])

# midgard supports
for i in [(353, 59), (355, 59), (355, 61), (357, 61), (357, 63), (359, 63)]:#, (282, 37), (284, 39), (286, 41), (288, 43)]:
    mx = (nodes[i[0]-1][0] + nodes[i[1]-1][0]) / 2
    my = (nodes[i[0]-1][1] + nodes[i[1]-1][1]) / 2
    mz = (nodes[i[0]-1][2] + nodes[i[1]-1][2]) / 2
    s_mid = [mx, my, mz]
    nodes.append(s_mid)
    elements['2x4'].append([i[0]-1, len(nodes) - 1, i[1]-1])

# bifrost
for i in [(236, 241), (233, 238), (270, 275), (267, 272), (300, 305), (297, 302), \
        (216, 221), (213, 218), (250, 255), (287, 252), (320, 325), (317, 322)]:
    mx = (nodes[i[0]-1][0] + nodes[i[1]-1][0]) / 2
    my = (nodes[i[0]-1][1] + nodes[i[1]-1][1]) / 2
    mz = (nodes[i[0]-1][2] + nodes[i[1]-1][2]) / 2
    s_mid = [mx, my, mz]
    nodes.append(s_mid)
    elements['2x4'].append([i[0]-1, len(nodes)-1, i[1]-1])

for i in [(236, 370, 241, 216, 376, 221), \
        (233, 371, 238, 213, 377, 218), \
        (89, 90, 91, 81, 82, 83), \
        (270, 372, 275, 250, 378, 255), \
        (267, 373, 272, 287, 379, 252), \
        (103, 104, 105, 111, 112, 97), \
        (300, 374, 305, 320, 380, 325), \
        (297, 375, 302, 317, 381, 322)]:
    n1 = nodes[i[0]-1]
    n2 = nodes[i[1]-1]
    n3 = nodes[i[2]-1]
    #n4 = nodes[i[3]-1]
    n5 = nodes[i[4]-1]
    #n6 = nodes[i[5]-1]
    vx = n3[0] - n1[0]
    vy = n3[1] - n1[1]
    norm = [vy, -vx]
    ln = math.sqrt(norm[0] ** 2 + norm[1] ** 2)
    end_n = [n2[0] + norm[0] / ln * 3, n2[1] + norm[1] / ln * 3, n2[2]]
    mx = (n2[0] + end_n[0]) / 2
    my = (n2[1] + end_n[1]) / 2
    mz = (n2[2] + end_n[2]) / 2

    nodes.append([mx, my, mz])
    nodes.append(end_n)
    elements['acry'].append([i[1]-1, len(nodes)-2, len(nodes)-1])

    mx = (n2[0] + n5[0]) / 2
    my = (n2[1] + n5[1]) / 2
    mz = (n2[2] + n5[2]) / 2
    nodes.append([mx, my, mz])
    elements['2x10'].append([i[1]-1, len(nodes)-1, i[4]-1])

# asgard
z_asg = nodes[113][2]
ldv = math.sqrt(nodes[116-1][0] ** 2 + nodes[116-1][1] ** 2)
udv = [nodes[116-1][0] / ldv, nodes[116-1][1] / ldv]
for n in [113, 115, 117, 119]:
    node = nodes[n-1]
    dp = node[0] * udv[0] + node[1] * udv[1]
    mn = [node[0] + udv[0] * (r_asg - dp), node[1] + udv[1] * (r_asg - dp), z_asg]
    mm = [(node[0] + mn[0]) / 2, (node[1] + mn[1]) / 2, z_asg]
    nodes.append(mm)
    nodes.append(mn)
    elements['2x4'].append([n-1, len(nodes)-2, len(nodes)-1])
for i in [(407, 409), (409, 411), (411, 413)]:
    mx = (nodes[i[0]-1][0] + nodes[i[1]-1][0]) / 2
    my = (nodes[i[0]-1][1] + nodes[i[1]-1][1]) / 2
    mz = (nodes[i[0]-1][2] + nodes[i[1]-1][2]) / 2
    s_mid = [mx, my, mz]
    nodes.append(s_mid)
    elements['2x4'].append([i[0]-1, len(nodes)-1, i[1]-1])

# asgard supports
for i in [(406, 97), (408, 97), (408, 99), (410, 99), (410, 101), (412, 101)]:
    mx = (nodes[i[0]-1][0] + nodes[i[1]-1][0]) / 2
    my = (nodes[i[0]-1][1] + nodes[i[1]-1][1]) / 2
    mz = (nodes[i[0]-1][2] + nodes[i[1]-1][2]) / 2
    s_mid = [mx, my, mz]
    nodes.append(s_mid)
    elements['2x4'].append([i[0]-1, len(nodes) - 1, i[1]-1])

# entrance to niflheim
for i in [2, 4, 147, 148, 20]:
    for idx in range(len(elements['2x4'])):
        if elements['2x4'][idx][1] == i - 1:
            del elements['2x4'][idx]
            break

# entrance to midgard
for i in [247, 248, 96]:
    for idx in range(len(elements['2x4'])):
        if elements['2x4'][idx][1] == i - 1:
            del elements['2x4'][idx]
            break

# output ccx input file
fout.write('*NODE,NSET=Nall\n')
for i, node in enumerate(nodes):
    node_line = str(i + 1) + ', ' + str(node[0]) + ', ' + str(node[1]) + ', ' + str(node[2]) + '\n'
    fout.write(node_line)

fout.write('*ELEMENT,TYPE=B32,ELSET=ETwoFour\n')
for i, el in enumerate(elements['2x4']):
    el_line = str(i + 1) + ', ' + str(el[0] + 1) + ', ' + str(el[1] + 1) + ', ' + str(el[2] + 1) + '\n'
    fout.write(el_line)

fout.write('*ELEMENT,TYPE=B32,ELSET=EFourFour\n')
for i, el in enumerate(elements['4x4']):
    el_num = i + 1 + len(elements['2x4'])
    el_line = str(el_num) + ', ' + str(el[0] + 1) + ', ' + str(el[1] + 1) + ', ' + str(el[2] + 1) + '\n'
    fout.write(el_line)

fout.write('*ELEMENT,TYPE=B32,ELSET=ETwoTen\n')
for i, el in enumerate(elements['2x10']):
    el_num = i + 1 + len(elements['2x4']) + len(elements['4x4'])
    el_line = str(el_num) + ', ' + str(el[0] + 1) + ', ' + str(el[1] + 1) + ', ' + str(el[2] + 1) + '\n'
    fout.write(el_line)

fout.write('*ELEMENT,TYPE=B32,ELSET=EAcry\n')
for i, el in enumerate(elements['acry']):
    el_num = i + 1 + len(elements['2x4']) + len(elements['4x4']) + len(elements['2x10'])
    el_line = str(el_num) + ', ' + str(el[0] + 1) + ', ' + str(el[1] + 1) + ', ' + str(el[2] + 1) + '\n'
    fout.write(el_line)

fout.write('*ELSET,ELSET=EAll,GENERATE\n')
fout.write('1,' + str(sum([len(elements[x]) for x in elements])) + '\n')

fout.write('*BOUNDARY\n')
for i in [1,3,5,7,9,11,13,15,346,348,350,352]:
    fout.write(str(i) + ',1,3\n')

fout.write('*MATERIAL,NAME=WOOD\n')
fout.write('*ELASTIC\n')
fout.write('1.8E8,.33\n')
fout.write('*DENSITY\n')
fout.write('34.\n')

fout.write('*MATERIAL,NAME=ACRY\n')
fout.write('*ELASTIC\n')
fout.write('6.0E7,.37\n')
fout.write('*DENSITY\n')
fout.write('74.3\n')

fout.write('*BEAM SECTION,ELSET=ETwoFour,MATERIAL=WOOD,SECTION=RECT\n')
fout.write('.292,.125\n')

fout.write('*BEAM SECTION,ELSET=EFourFour,MATERIAL=WOOD,SECTION=RECT\n')
fout.write('.292,.292\n')

fout.write('*BEAM SECTION,ELSET=ETwoTen,MATERIAL=WOOD,SECTION=RECT\n')
fout.write('.771,.125\n')

fout.write('*BEAM SECTION,ELSET=EAcry,MATERIAL=ACRY,SECTION=RECT\n')
fout.write('.333,.833\n') # 4" x 10"

fout.write('*STEP\n')
fout.write('*STATIC\n')

fout.write('*DLOAD\n')
fout.write('EAll,GRAV,3.22E1,0.,0.,-1.\n')

fout.write('*CLOAD\n')
# midgard
load = math.pi * 9 * 100
fout.write('354,3,-' + str(load / 4 / 6) + '\n')
fout.write('356,3,-' + str(load / 4 / 3) + '\n')
fout.write('358,3,-' + str(load / 4 / 3) + '\n')
fout.write('360,3,-' + str(load / 4 / 6) + '\n')
fout.write('353,3,-' + str(load / 2 / 6) + '\n')
fout.write('355,3,-' + str(load / 2 / 3) + '\n')
fout.write('357,3,-' + str(load / 2 / 3) + '\n')
fout.write('359,3,-' + str(load / 2 / 6) + '\n')
fout.write('75,3,-' + str(load / 4 / 6) + '\n')
fout.write('77,3,-' + str(load / 4 / 3) + '\n')
fout.write('79,3,-' + str(load / 4 / 3) + '\n')
fout.write('65,3,-' + str(load / 4 / 6) + '\n')
#print 'midgard:', load
# bifrost
fout.write('382,3,-200.\n')
fout.write('385,3,-200.\n')
fout.write('388,3,-200.\n')
fout.write('391,3,-200.\n')
fout.write('394,3,-200.\n')
fout.write('397,3,-200.\n')
fout.write('400,3,-200.\n')
fout.write('403,3,-200.\n')
# asgard
load = math.pi * 4 * 100
fout.write('407,3,-' + str(load / 4 / 6) + '\n')
fout.write('409,3,-' + str(load / 4 / 3) + '\n')
fout.write('411,3,-' + str(load / 4 / 3) + '\n')
fout.write('413,3,-' + str(load / 4 / 6) + '\n')
fout.write('406,3,-' + str(load / 2 / 6) + '\n')
fout.write('408,3,-' + str(load / 2 / 3) + '\n')
fout.write('410,3,-' + str(load / 2 / 3) + '\n')
fout.write('412,3,-' + str(load / 2 / 6) + '\n')
fout.write('113,3,-' + str(load / 4 / 6) + '\n')
fout.write('115,3,-' + str(load / 4 / 3) + '\n')
fout.write('117,3,-' + str(load / 4 / 3) + '\n')
fout.write('119,3,-' + str(load / 4 / 6) + '\n')
#print 'asgard:', load

fout.write('*EL PRINT,ELSET=ETwoFour\n')
fout.write('S\n')

fout.write('*EL PRINT,ELSET=ETwoTen\n')
fout.write('S\n')

fout.write('*EL FILE\n')
fout.write('S\n')

fout.write('*NODE FILE\n')
fout.write('U\n')

fout.write('*END STEP\n')
