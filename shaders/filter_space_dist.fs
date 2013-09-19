/////SPATIAL DISTORTION FILTER/////
//http://pixelshaders.com

precision mediump float;

varying vec2 uv;

uniform sampler2D tex0;
uniform vec3 unif[20];
// time unif[16][0]

float t = unif[16][0];

void main(void) {
  vec2 newuv = uv + vec2(sin(uv.y * 80.0 + t * 6.0) * 0.03, 0.0);
  gl_FragColor = texture2D(tex0, newuv);
  gl_FragColor.a = unif[5][2];
}
