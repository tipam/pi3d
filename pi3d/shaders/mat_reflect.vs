#include std_head_vs.inc

varying vec2 bumpcoordout;
varying vec3 inray;
varying vec3 normout;
varying float dist;
varying vec3 lightVector;
varying float lightFactor;

void main(void) {
#include std_main_vs.inc
  bumpcoordout = (texcoord * unib[2].xy + unib[3].xy) * vec2(1.0, 1.0) * unib[0][0];

  inray = vec3(relPosn - vec4(unif[6], 0.0)); // ----- vector from the camera to this vertex
  dist = length(inray);
  inray = normalize(inray);

  gl_Position = modelviewmatrix[1] * vec4(vertex, 1.0);
  gl_PointSize = unib[2][2] / dist;
}
