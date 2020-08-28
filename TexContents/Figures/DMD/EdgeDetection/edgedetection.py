import imageio
import numpy as np
import matplotlib.pyplot as plt


def detectEdges(image, radius, threshold):
    result = image.copy()
    h = len(image)
    w = len(image[0])
    for y in range(h):
        print(y)
        for x in range(w):
            varea = (2*radius + 1)**2
            harea = varea
            vsum = 0
            hsum = 0
            for j in range(y-radius,y+radius+1):
                for i in range(x-radius,x+radius+1):
                    if i < 0 or j < 0 or i >= w or j >= h:
                        varea = varea - 1
                        harea = harea - 1
                    else:
                        if 2*x - i < 0 or 2*x - i >= w:
                            harea = harea - 1
                        else:
                            hsum = hsum + abs(image[j][i] - image[j][2*x-i])
                        
                        if 2*y - j < 0 or 2*y - j >= h:
                            varea = varea - 1
                        else:
                            vsum = vsum + abs(image[j][i] - image[2*y - j][i])
            result[y][x] = 1*(hsum / harea > threshold or vsum / varea > threshold) 
    return result


test = imageio.imread('../mapping/twoshapes-target.png')
res = detectEdges(test, 10, 35)

plt.imshow(res)
plt.show()
