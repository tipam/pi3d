precision highp float;

attribute vec3 vertex;
attribute vec3 normal;
attribute vec2 texcoord;

uniform mat4 modelviewmatrix;
uniform mat4 cameraviewmatrix;
uniform vec3 unif[11];

varying vec3 normout;
varying vec3 lightVector;
varying float dist;

void main(void) {
  
  //lightVector = normalize(vec3(cameraviewmatrix * vec4(unif[8], 1.0))); // ------ rotate relative to view
  lightVector = normalize(unif[8]); // ------ rotate relative to view
  normout = normalize(vec3(modelviewmatrix * vec4(normal, 0.0)));   
  vec4 relPosn = modelviewmatrix * vec4(vertex,1.0);
  dist = length(relPosn);
  gl_Position = relPosn;
}
