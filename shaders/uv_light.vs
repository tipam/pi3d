precision highp float;

attribute vec3 vertex;
attribute vec3 normal;
attribute vec2 texcoord;

uniform mat4 modelviewmatrix[2]; // 0 model movement in real coords, 1 in camera coords
uniform vec3 unif[11];

varying vec3 normout;
varying vec2 texcoordout;
varying vec3 lightVector;
varying float dist;

void main(void) {
  vec4 relPosn = modelviewmatrix[0] * vec4(vertex,1.0);
  
  lightVector = normalize(unif[8]); 
  normout = normalize(vec3(modelviewmatrix[0] * vec4(normal, 0.0)));   

  vec3 inray = vec3(relPosn - vec4(unif[6], 0.0)); // ----- vector from the camera to this vertex
  dist = length(inray);

  texcoordout = texcoord;

  gl_Position = modelviewmatrix[1] * vec4(vertex,1.0);
}
