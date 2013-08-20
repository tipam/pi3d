precision highp float;

attribute vec3 vertex;
attribute vec3 normal;
attribute vec2 texcoord;

uniform mat4 modelviewmatrix[2]; // 0 model movement in real coords, 1 in camera coords
uniform vec3 unib[4];
//uniform float ntiles => unib[0][0]
//uniform vec2 umult, vmult => unib[2]
//uniform vec2 u_off, v_off => unib[3]
uniform vec3 unif[16];
//uniform vec3 lightpos > unif[8]

varying vec2 texcoordout;
varying vec2 bumpcoordout;
varying float dist;
varying vec3 lightVector;

void main(void) {
  vec4 relPosn = modelviewmatrix[0] * vec4(vertex,1.0);
  
  lightVector = normalize(unif[8]); 
  lightVector.z *= -1.0;
  vec3 normout = normalize(vec3(modelviewmatrix[0] * vec4(normal, 0.0)));   
  vec3 bnorm = vec3(0.0, 0.0, 1.0); // ----- normal to original bump map sheet
  float c = dot(bnorm, normout); // ----- cosine
  float t = 1.0 - c;
  vec3 a = cross(bnorm, normout); // ----- axis
  float s = length(a); // ----- sine (depends on bnorm and normout being unit vectors)
  if (s > 0.0) a = normalize(a);
  lightVector = vec3(mat4(
    t * a.x * a.x + c, t * a.x * a.y + a.z * s, t * a.x * a.z - a.y * s, 0.0,
    t * a.x * a.y - a.z * s, t * a.y * a.y + c, t * a.z * a.y + a.x * s, 0.0,
    t * a.x * a.z + a.y * s, t * a.y * a.z - a.x * s, t * a.z * a.z + c, 0.0,
    0.0, 0.0, 0.0, 1.0) * vec4(lightVector, 0.0)); // ----- vector mult for rotation about axis
  bumpcoordout = (texcoord * unib[2].xy + unib[3].xy) * vec2(1.0, -1.0) * unib[0][0];

  vec3 inray = vec3(relPosn - vec4(unif[6], 0.0)); // ----- vector from the camera to this vertex
  dist = length(inray);

  texcoordout = texcoord * unib[2].xy + unib[3].xy;

  gl_Position = modelviewmatrix[1] * vec4(vertex,1.0);
  gl_PointSize = unib[2][2] / dist;
}
