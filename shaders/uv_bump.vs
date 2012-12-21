precision highp float;

attribute vec3 vertex;
attribute vec3 normal;
attribute vec2 texcoord;

uniform mat4 modelviewmatrix;
uniform mat4 cameraviewmatrix;
uniform vec3 unib[2];
//uniform float ntiles => unib[0][0]
uniform vec3 unif[11];
//uniform vec3 lightpos > unif[8]

varying vec3 normout;
varying vec2 texcoordout;
varying vec2 bumpcoordout;
varying mat4 normrot;
varying float dist;
varying vec3 lightVector;

void main(void) {
  
  l//ightVector = normalize(vec3(cameraviewmatrix * vec4(unif[8], 0.0))); // ------ rotate relative to view
  lightVector = normalize(unif[8]);
  normout = normalize(vec3(modelviewmatrix * vec4(normal, 0.0)));   

  vec3 bnorm = vec3(0.0, 0.0, 1.0); // ----- normal to original bump map sheet
  float c = dot(bnorm, normout); // ----- cosine
  float t = 1.0 - c;
  vec3 a = cross(bnorm, normout); // ----- axis
  float s = length(a); // ----- sine (depends on bnorm and normout being unit vectors)
  a = normalize(a);
  normrot = mat4(
    t * a.x * a.x + c, t * a.x * a.y + a.z * s, t * a.x * a.z - a.y * s, 0.0,
    t * a.x * a.y - a.z * s, t * a.y * a.y + c, t * a.z * a.y + a.x * s, 0.0,
    t * a.x * a.z + a.y * s, t * a.y * a.z - a.x * s, t * a.z * a.z + c, 0.0,
    0.0, 0.0, 0.0, 1.0); // ----- vector mult for rotation about axis
  bumpcoordout = texcoord * unib[0][0];

  texcoordout = texcoord;

  vec4 relPosn = modelviewmatrix * vec4(vertex,1.0);
  dist = length(relPosn);
  gl_Position = relPosn;
}
