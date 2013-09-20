/////DISPLACEMENT FILTER/////
//http://pixelshaders.com

precision mediump float;

varying vec2 uv;

uniform sampler2D tex0;
uniform vec3 unif[20];
// time unif[16][0]

float t = unif[16][0];

float stripes(vec2 p, float steps) {
  return fract(p.x*steps);
}

void main(void) {
  vec4 color = texture2D(tex0, uv);

  float brightness = stripes(uv + vec2(color.r * 0.1 * sin(t), 0.0), 10.0);
  gl_FragColor.rgb = vec3(brightness);
  gl_FragColor.a = unif[5][2];
}
