/////DISPLACEMENT FILTER/////
//http://pixelshaders.com

precision mediump float;

varying vec2 uv;

uniform sampler2D tex0;
uniform vec3 unif[20];
// time unif[16][0]
// size unif[16][1]

float t = unif[16][0];
float size = unif[16][1];

float wrap(float x) {
  return abs(mod(x, 2.0) - 1.0);
}

void main(void) {
  vec2 p = uv;

  p.x = mod(p.x, size);
  p.x = abs(p.x - size / 2.0);
  p.x = wrap(p.x + t / 6.0);

  gl_FragColor = texture2D(tex0, p);
  gl_FragColor.a = unif[5][2];
}
