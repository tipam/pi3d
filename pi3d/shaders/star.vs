precision mediump float;

attribute vec3 vertex;
attribute vec2 texcoord;

uniform mat4 modelviewmatrix[2]; // 0 model movement in real coords, 1 in camera coords
uniform vec3 unib[4];
//uniform vec2 umult, vmult => unib[2]
//uniform vec2 u_off, v_off => unib[3]
uniform vec3 unif[20];    // hpe
//uniform float time =========> unif[16][0]
//uniform float fScale =======> unif[16][1]
//uniform float fOriginShift => unif[16][2]

varying vec2 texcoordout;

void main(void) {
  texcoordout = texcoord * unib[2].xy + unib[3].xy;

  // The texture scale, the bigger the value -> more waves
  float fScale = unif[16][1];
 
  // Set the orgin of the star. To get a "real" star we need a shift from 0,0 -> -0.5, -0.5
  float fOrginShift = unif[16][2];
 
  // compute the position
  texcoordout = fOrginShift  + texcoordout * fScale;

  gl_Position = modelviewmatrix[1] * vec4(vertex,1.0);
}
