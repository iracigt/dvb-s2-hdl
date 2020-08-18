f = firdes.root_raised_cosine(1, 2, 1, 0.2, 31)
scaled = [x / max(f) for x in f]
mem = ['{:04X}'.format(twos(round((2**15-1) * x))) for x in scaled]
print('\n'.join(mem))
