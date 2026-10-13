import numpy as np
from PIL import Image, ImageOps
from math import floor
from math import ceil
import random
img_mat= np.zeros((2500,2500,3), dtype=np.uint8)
z_buffer=np.full((2500,2500),np.inf , dtype=np.float32)
def BC(x0,y0,x1,y1,x2,y2,x,y,d):
    lambda0=(((x-x2)*(y1-y2)-(x1-x2)*(y-y2))/d)
    lambda1=(((x0-x2)*(y-y2)-(x-x2)*(y0-y2))/d)
    lambda2=1.0-lambda0-lambda1
    return lambda0,lambda1,lambda2

def calculate_normal(p0,p1,p2):
    v1=(p1[0]-p2[0], p1[1]-p2[1],p1[2]-p2[2])
    v2=(p1[0]-p0[0],p1[1]-p0[1],p1[2]-p0[2])
    normal=np.cross(v1,v2)
    return normal

def draw_triangle(img_mat, z_buffer, x0,y0,z0,x1,y1,z1,x2,y2,z2,cos):
    color=(-255*cos,0,0)
    height=len(img_mat)
    width=len(img_mat[0])
    xmin=floor(max(0,min(x0,x1,x2)))
    ymin=floor(max(0,min(y0,y1,y2)))
    xmax=ceil(min(width-1, max(x0,x1,x2)))
    ymax=ceil(min(height-1,max(y0,y1,y2)))


    denom=((x0-x2)*(y1-y2)-(x1-x2)*(y0-y2))
    if denom==0:
        return
    for y in range(ymin, ymax+1):
        for x in range(xmin, xmax+1):
            l0,l1,l2=BC(x0,y0,x1,y1,x2,y2,x+0.5,y+0.5,denom)

            if l0>=0 and l1>=0 and l2>=0:
                z_hat=l0*z0+l1*z1+l2*z2
                if z_hat<z_buffer[y][x]:
                    z_buffer[y][x]=z_hat
                    img_mat[y][x]=color





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
   z0=(v[f[i][0]-1][2])*6000+1250
   x1=(v[f[i][1]-1][0])*6000+1250
   y1=(v[f[i][1]-1][1])*6000+1250
   z1=(v[f[i][1]-1][2])*6000+1250
   x2=(v[f[i][2]-1][0])*6000+1250
   y2=(v[f[i][2]-1][1])*6000+1250
   z2=(v[f[i][2]-1][2])*6000+1250

   p0=(x0,y0,z0)
   p1=(x1,y1,z1)
   p2=(x2,y2,z2)
   l=np.array([0,0,1])
   n=calculate_normal(p0,p1,p2)
   norm_n=np.linalg.norm(n)
   norm_l=np.linalg.norm(l)
   cos=(np.dot(n,l))/(norm_n*norm_l)
   if cos<0:
       draw_triangle(img_mat,z_buffer,x0,y0,z0,x1,y1,z1,x2,y2,z2,cos)


#def line(img_mat,x0,y0,x1,y1):
 #   d_max=max(abs(floor(x0)-floor(x1)),abs(floor(y0)-floor(y1)))
 #   x,y=x0,y0
 #   L=d_max+1 
 #   if(L==1):
 #       img_mat[floor(y0),floor(x0)]=255
 #   else:    
 #       dx=(x1-x0)/(L-1)
 #       dy=(y1-y0)/(L-1)  
 #       for _ in range(0,L):
 #           img_mat[floor(y),floor(x)]=255
 #           x+=dx
 #           y+=dy
#for i in range(len(v)):
    #x=v[i][0]*6000+750
    #y=-v[i][1]*6000+750
    #img_mat[floor(y),floor(x)]=35,255,35

img=Image.fromarray(img_mat)
img=ImageOps.flip(img)
img.save('img.png')