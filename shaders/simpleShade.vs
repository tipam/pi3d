precision highp float;

attribute vec3 vertex;
attribute vec3 normal;
attribute vec2 texcoord;

uniform mat4 modelviewmatrix;
uniform mat4 cameraviewmatrix;
uniform vec3 unib[2];
//uniform float ntiles => unib[0][0]
//uniform float shiny ==> unib[0][1]
uniform vec3 unif[11];
//uniform vec3 locn ====> unif[0]
//uniform vec3 rotn ====> unif[1]
//uniform vec3 scle ====> unif[2]
//uniform vec3 ofst ====> unif[3]
//uniform vec3 eye =====> unif[6]
//uniform vec3 rtn =====> unif[7]
//uniform vec3 lightpos > unif[8]

varying vec3 normout;
varying vec2 texcoordout;
varying vec2 bumpcoordout;
varying mat4 normrot;
varying vec2 shinecoordout;
varying float dist;
varying vec3 lightVector;

void main(void) {
  
  lightVector = normalize(vec3(cameraviewmatrix * vec4(unif[8], 0.0))); // ------ rotate relative to view

  bumpcoordout = texcoord;
  normrot = mat4(1.0);
  shinecoordout = vec2(0.0, 0.0);
  texcoordout = texcoord;
  gl_Position = modelviewmatrix * vec4(vertex,1.0);
}
