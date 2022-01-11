# mesh_render.py


import numpy as np
from glumpy import app, gl, glm, gloo, data
from glumpy.geometry import primitives
from glumpy.app.movie import record
arr = np.array([[-1,-1],[0,0],[0.5,1],[1,1]])
r = 10
p = np.array([[[  10.,  50.], [  10., 350.]]])
w = 6



vertex0 = """
    attribute vec2 position;
    attribute float size;


    varying vec2 center;
    varying float radius;
    void main() {
        gl_Position = vec4(position, 0.0, 1.0);
        gl_PointSize = 2.0+ceil(size);
        center = 500 + position*500;
        radius = size/2.0;
    } """

fragment0 = """
  float coverage(float d, float antialias)
  {
      d = d + antialias;
      float alpha = d/antialias;
      if( d < 0.0 ) return 1.0;
      return exp(-alpha*alpha);
  }

  float circle(vec2 p, vec2 center, float radius)
  {
      return length(p - center) - radius;
  }

  varying vec2 center;
  varying float radius;

  void main()
  {
      vec2 p = gl_FragCoord.xy;
      float antialias = 1.0;
      if (radius < 1.0) {
          float d = circle(p, center, 1.0);
          gl_FragColor = vec4(vec3(0.0), radius*coverage(d, 1.0));
      } else {
          float d = circle(p, center, radius);
          gl_FragColor = vec4(vec3(0.0), coverage(d, 1.0));
      }
  } """
app.use("osxglut")
window = app.Window(1000, 1000, color=(1,1,1,1))
V0 = np.zeros(len(arr), [("position", np.float32, 2),
                 ("size",     np.float32, 1)])
V0["position"] = arr
V0["size"] = np.zeros(len(arr))+r
points = gloo.Program(vertex0, fragment0)
V0 = V0.view(gloo.VertexBuffer)
points['position'] = V0["position"] 
points['size'] = V0["size"] 


vertex1 = """
uniform vec2 resolution;
uniform float antialias;

attribute float thickness;
attribute vec2 p0, p1, uv;

varying float v_alpha, v_thickness;
varying vec2 v_p0, v_p1, v_p;

void main() {

  if( abs(thickness) < 1.0 ) {
     v_thickness = 1.0;
     v_alpha = abs(thickness);
  } else {
     v_thickness = abs(thickness);
     v_alpha = 1.0;
  } 

  float t = v_thickness/2.0 + antialias;
  float l = length(p1-p0);
  float u = 2.0*uv.x - 1.0;
  float v = 2.0*uv.y - 1.0;

  // Screen space
  vec2 T = normalize(p1-p0);
  vec2 O = vec2(-T.y , T.x);
  vec2 p = p0 + vec2(0.5,0.5) + uv.x*T*l + u*T*t + v*O*t;
  gl_Position = vec4(2.0*p/resolution-1.0, 0.0, 1.0);

  // Local space
  T = vec2(1.0, 0.0);
  O = vec2(0.0, 1.0);
  p = uv.x*T*l + u*T*t + v*O*t;

  v_p0 = vec2(0.0, 0.0);
  v_p1 = vec2(  l, 0.0);
  v_p  = p;
} """

fragment1 = """
uniform float antialias;
varying float v_alpha, v_thickness;
varying vec2 v_p0, v_p1, v_p;
void main() {
  float d = 0;
  if( v_p.x < 0 )
      d = length(v_p - v_p0) - v_thickness/2.0 + antialias/2.0;
  else if ( v_p.x > length(v_p1-v_p0) )
      d = length(v_p - v_p1) - v_thickness/2.0 + antialias/2.0;
  else
      d = abs(v_p.y) - v_thickness/2.0 + antialias/2.0;
  if( d < 0)
      gl_FragColor = vec4(0.0, 0.0, 0.0, v_alpha);
  else if (d < antialias) {
      d = exp(-d*d);
      gl_FragColor = vec4(0.0, 0.0, 0.0, d*v_alpha);
  } 
} """




#####################
n = len(p) 
V = np.zeros((n, 4), dtype=[('p0', np.float32, 2),
                           ('p1', np.float32, 2),
                           ('uv', np.float32, 2),
                           ('thickness', np.float32, 1)])
V["p0"] = p[:,0].ravel().reshape(n,1,2)
V["p1"] = p[:,1].ravel().reshape(n,1,2)
V["uv"] = (0,0), (0,1), (1,0), (1,1)
V["thickness"] = np.zeros(n).reshape(n,1) + w
#####
print(V)
segments = gloo.Program(vertex1, fragment1, count=n)
segments.bind(V.ravel().view(gloo.VertexBuffer))
segments["antialias"] = 2.0

I = np.zeros((n,6), dtype=np.uint32)
I[:] = [0,1,2,1,2,3]
I += 4*np.arange(n,dtype=np.uint32).reshape(n,1)
I = I.ravel().view(gloo.IndexBuffer)

@window.event
def on_resize(width, height):
    segments["resolution"] = width, height

@window.event
def on_draw(dt):
    window.clear()
    segments.draw(gl.GL_TRIANGLES, I)
    points.draw(gl.GL_POINTS)
duration = 5.0
framerate = 60
with record(window, "cube.mp4", fps=framerate):
    app.run(framerate=framerate, duration=duration)