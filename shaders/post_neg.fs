precision mediump float;

varying vec2 texcoordout;

uniform sampler2D tex0;
uniform vec3 unif[20];
//uniform vec3 custom use ==> unif[16] to unif[19]

void main(void) {
  ///////////////////////////////////////////////////////////////////
  // you can do processing on the texture (or utilise other textures)
  // here. This skeleton just does a fairly approximate convolution
  // with a variable offset distance
  ///////////////////////////////////////////////////////////////////
  gl_FragColor = step(vec4(0.9, 0.9, 0.9, 0.9), vec4(1.0, 1.0, 1.0, 1.0) - texture2D(tex0, texcoordout));
  gl_FragColor.a = 1.0;
}


