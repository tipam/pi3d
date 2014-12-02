#include std_head_vs.inc

varying vec3 lightVector;
varying float dist;
varying float lightFactor;

void main(void) {
  vec3 normout;
#include std_main_vs.inc

  vec3 inray = vec3(relPosn - vec4(unif[6], 0.0)); // ----- vector from the camera to this vertex
  dist = length(inray);
  
  gl_Position = modelviewmatrix[1] * vec4(vertex,1.0);
  gl_PointSize = unib[2][2] / dist;
}
