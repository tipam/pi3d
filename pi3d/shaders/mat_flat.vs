#include std_head_vs.inc

varying float dist;

void main(void) {
  vec4 relPosn = modelviewmatrix[0] * vec4(vertex,1.0);
  vec3 inray = vec3(relPosn - vec4(unif[6], 0.0)); // ----- vector from the camera to this vertex
  dist = length(inray);
  gl_Position = modelviewmatrix[1] * vec4(vertex,1.0);
  gl_PointSize = clamp(unib[2][2] / dist, 1.0, unib[2][2]);
}
