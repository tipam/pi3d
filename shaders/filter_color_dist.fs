/////COLOR DISTORTION FILTER/////
//http://pixelshaders.com

precision mediump float;

varying vec2 uv;

uniform sampler2D tex0;
uniform vec3 unif[20];
// distortion amount rgb unif[16]

vec3 dist = unif[16];

float wave(float x, float amount) {
  return (sin(x * amount) + 1.0) * .5;
}

void main(void) {
  vec4 color = texture2D(tex0, uv);
  gl_FragColor.r = wave(color.r, dist.r);
  gl_FragColor.g = wave(color.g, dist.g);
  gl_FragColor.b = wave(color.b, dist.b);
  gl_FragColor.a = unif[5][2];
}
