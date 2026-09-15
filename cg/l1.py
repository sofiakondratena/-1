import numpy as np
from PIL import Image
from math import floor
img_mat= np.zeros((2500,2500,3), dtype=np.uint8)
def line(img_mat,x0,y0,x1,y1):
    d_max=max(abs(floor(x0)-floor(x1)),abs(floor(y0)-floor(y1)))
    x,y=x0,y0
    L=d_max+1 
    if(L==1):
        img_mat[floor(y0),floor(x0)]=255
    else:    
        dx=(x1-x0)/(L-1)
        dy=(y1-y0)/(L-1)  
        for _ in range(0,L):
            img_mat[floor(y),floor(x)]=255
            x+=dx
            y+=dy
v=[]
f=[]
file=open('model.obj')
for s in file:
    sp=s.split()
    if(sp[0]=='v'):
        v.append([float(sp[1]),float(sp[2]),float(sp[3])])
    elif(sp[0]=='f'):
        f.append([int(sp[1].split("/")[0]),int(sp[2].split("/")[0]),int(sp[3].split("/")[0])])
for i in range(len(f)):
    x0=(v[f[i][0]-1][0])*6000+1250
    y0=(v[f[i][0]-1][1])*6000+1250
    x1=(v[f[i][1]-1][0])*6000+1250
    y1=(v[f[i][1]-1][1])*6000+1250
    x2=(v[f[i][2]-1][0])*6000+1250
    y2=(v[f[i][2]-1][1])*6000+1250
    line(img_mat,x0,y0,x1,y1)
    line(img_mat,x1,y1,x2,y2)
    line(img_mat,x2,y2,x0,y0)
#for i in range(len(v)):
    #x=v[i][0]*6000+750
    #y=-v[i][1]*6000+750
    #img_mat[floor(y),floor(x)]=35,255,35
img=Image.fromarray(img_mat)
img.save('img.png')