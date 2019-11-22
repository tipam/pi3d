#version 120
//precision mediump float;

uniform vec3 unib[5];
//uniform float hardness => unib[0][0]
//uniform float discard => unib[0][2]

varying vec4 colour;

//fragcolor

void main(void) {
  float alpha = 2.0 * unib[0][0] * (0.5 - length(gl_PointCoord - vec2(0.5)));
  if (alpha < unib[0][2]) discard; // ------ to allow rendering behind the transparent parts of this object
  gl_FragColor = colour;
  gl_FragColor.a *= alpha;
}