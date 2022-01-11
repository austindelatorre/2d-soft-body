# -----------------------------------------------------------------------------
# Python & OpenGL for Scientific Visualization
# www.labri.fr/perso/nrougier/python+opengl
# Copyright (c) 2017, Nicolas P. Rougier
# Distributed under the 2-Clause BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, gloo, gl

vertex = """
    attribute vec2 position;
    attribute float size;


    varying vec2 center;
    varying float radius;
    void main() {
        gl_Position = vec4(position, 0.0, 1.0);
        gl_PointSize = 2.0+ceil(size);
        center = 300 + position*300;
        radius = size/2.0;
    } """

fragment = """
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

arr = np.array([[0,0],[0.5,1]])
r = 30

def render_dots(arr, r):
  window = app.Window(600, 600, color=(1,1,1,1))
  V = np.zeros(len(arr), [("position", np.float32, 2),
                     ("size",     np.float32, 1)])
  V["position"] = arr
  V["size"] = np.zeros(len(arr))+r
  points = gloo.Program(vertex, fragment)
  V = V.view(gloo.VertexBuffer)
  points['position'] = V["position"] 
  points['size'] = V["size"] 

  @window.event
  def on_draw(dt):
    window.clear()
    points.draw(gl.GL_POINTS)
  app.run()
