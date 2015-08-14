#include std_head_vs.inc

varying vec2 texcoordout;
varying vec2 bumpcoordout;
varying float dist;
varying vec3 lightVector;
varying vec3 normout;
varying vec3 inray;
varying float lightFactor;

void main(void) {
#include std_main_vs.inc
  bumpcoordout = (texcoord * unib[2].xy + unib[3].xy) * vec2(1.0, 1.0) * unib[0][0];

  inray = normalize(relPosn.xyz - unif[6]); // ----- vector from the camera to this vertex

  texcoordout = texcoord * unib[2].xy + unib[3].xy;

  gl_Position = modelviewmatrix[1] * vec4(vertex,1.0);
  dist = gl_Position.z;
  gl_PointSize = unib[2][2] / dist;
}
