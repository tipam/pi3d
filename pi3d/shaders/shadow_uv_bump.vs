#include std_head_vs.inc

varying vec2 texcoordout;
varying vec2 bumpcoordout;
varying float dist;
varying vec3 lightVector;
varying float lightFactor;

varying vec4 shadowposn;

void main(void) {
  vec3 normout;
#include std_main_vs.inc
  bumpcoordout = (texcoord * unib[2].xy + unib[3].xy) * vec2(1.0, 1.0) * unib[0][0];

  vec3 inray = vec3(relPosn - vec4(unif[6], 0.0)); // ----- vector from the camera to this vertex
  dist = length(inray);

  texcoordout = texcoord * unib[2].xy + unib[3].xy;
  shadowposn = modelviewmatrix[2] * vec4(vertex, 1.0);

  gl_Position = modelviewmatrix[1] * vec4(vertex,1.0);
  gl_PointSize = unib[2][2] / dist;
}
