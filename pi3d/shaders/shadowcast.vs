#include std_head_vs.inc

varying vec2 texcoordout;
varying vec2 bumpcoordout;
varying vec2 shadcoordout;
varying float dist;
varying vec3 lightVector;

void main(void) {
  vec4 relPosn = modelviewmatrix[0] * vec4(vertex,1.0);
  float left = unif[16][0];
  float top = unif[16][1];
  float rflag = unif[16][2];
  float right = unif[17][0];
  float bottom = unif[17][1];
  float offset = unif[17][2] * vertex.y;
  
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

  if (rflag > 0.5) { // ------ shadows rotated 90 degrees
    shadcoordout = vec2(texcoord[1] * (top - bottom) + bottom,
                        texcoord[0] * (right - left) + left + offset);
  }
  else { // ------ shadows not rotated
    shadcoordout = vec2(texcoord[0] * (top - bottom) + bottom,
                        texcoord[1] * (right - left) + left + offset);
  }

  gl_Position = modelviewmatrix[1] * vec4(vertex,1.0);
}
