pl_hdr = array([ 0.707+0.707j,  0.707-0.707j, -0.707-0.707j, -0.707+0.707j,
        0.707+0.707j, -0.707+0.707j, -0.707-0.707j,  0.707-0.707j,
        0.707+0.707j,  0.707-0.707j,  0.707+0.707j, -0.707+0.707j,
       -0.707-0.707j, -0.707+0.707j, -0.707-0.707j,  0.707-0.707j,
       -0.707-0.707j, -0.707+0.707j, -0.707-0.707j, -0.707+0.707j,
        0.707+0.707j, -0.707+0.707j,  0.707+0.707j, -0.707+0.707j,
       -0.707-0.707j, -0.707+0.707j,  0.707+0.707j,  0.707-0.707j,
        0.707+0.707j, -0.707+0.707j,  0.707+0.707j, -0.707+0.707j,
       -0.707-0.707j, -0.707+0.707j, -0.707-0.707j, -0.707+0.707j,
       -0.707-0.707j, -0.707+0.707j, -0.707-0.707j,  0.707-0.707j,
       -0.707-0.707j, -0.707+0.707j, -0.707-0.707j, -0.707+0.707j,
       -0.707-0.707j,  0.707-0.707j,  0.707+0.707j, -0.707+0.707j,
        0.707+0.707j, -0.707+0.707j, -0.707-0.707j,  0.707-0.707j,
       -0.707-0.707j,  0.707-0.707j, -0.707-0.707j, -0.707+0.707j,
       -0.707-0.707j, -0.707+0.707j, -0.707-0.707j, -0.707+0.707j,
        0.707+0.707j,  0.707-0.707j, -0.707-0.707j,  0.707-0.707j,
       -0.707-0.707j,  0.707-0.707j, -0.707-0.707j, -0.707+0.707j,
        0.707+0.707j, -0.707+0.707j, -0.707-0.707j,  0.707-0.707j,
       -0.707-0.707j, -0.707+0.707j, -0.707-0.707j,  0.707-0.707j,
       -0.707-0.707j, -0.707+0.707j,  0.707+0.707j, -0.707+0.707j,
        0.707+0.707j,  0.707-0.707j,  0.707+0.707j, -0.707+0.707j,
       -0.707-0.707j,  0.707-0.707j,  0.707+0.707j,  0.707-0.707j,
       -0.707-0.707j, -0.707+0.707j], dtype=complex64)

code = []

for p in pl_hdr:
    i, q = np.real(p), np.imag(p)
    if (i > 0 and q > 0):
        code.append(0)
    if (i < 0 and q > 0):
        code.append(6)
    if (i < 0 and q < 0):
        code.append(3)
    if (i > 0 and q < 0):
        code.append(5)

for i, c in enumerate(code):
      print("initial tbl[{}]  = 3'd{};".format(i, c))
