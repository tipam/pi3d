precision mediump float;

varying vec2 texcoordout;

uniform sampler2D tex0;
uniform vec3 unif[20];
//uniform vec3 custom use ==> unif[16] to unif[19]

void main(void) {
  gl_FragColor = vec4(1.0, 1.0, 1.0, 1.0) - texture2D(tex0, texcoordout);
  gl_FragColor.a = unif[5][2];
}


