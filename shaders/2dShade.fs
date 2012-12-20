precision mediump float;

varying vec2 texcoordout;

uniform sampler2D tex0;
uniform mat4 cameraviewmatrix;
uniform vec3 unib[2];
//uniform float ntiles ===> unib[0][0]
//uniform float shiny ====> unib[0][1]
//uniform float blend ====> unib[0][2]

void main(void) {
  vec4 texc = texture2D(tex0, texcoordout); // ------ material or basic colour from texture
  float alpha = texc[3];
  if (alpha < unib[0][2]) discard; // ------ to allow rendering behind the transparent parts of this object
  gl_FragColor = texc;
}


