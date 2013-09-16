/////CRYSTALOGRAPHY FILTER/////
//http://pixelshaders.com

precision mediump float;

varying vec2 uv;

uniform sampler2D tex0;
uniform vec3 unif[20];
// time unif[16][0]
// scale unif[16][1]
// limit unif[16][2]

float t = unif[16][0];
float scale = unif[16][1];
float limit = unif[16][2];

float wave(vec2 p, float angle) {
  vec2 direction = vec2(cos(angle), sin(angle));
  return cos(dot(p, direction));
}

float wrap(float x) {
  return abs(mod(x, 2.0) - 1.0);
}

void main(void) {
  vec4 color = texture2D(tex0, uv);
  
  vec2 p = (uv - 0.5) * scale;

  float brightness = wave(p, t) + wave(p, t * 0.5) + wave(p, t * 0.3333) +
                wave(p, t * 0.25) + wave(p, t * 0.2) + wave(p, t * 0.16666) +
                wave(p, t * 0.14286) + wave(p, t * 0.125) + wave(p, t * 0.11111);

  brightness = clamp(wrap(brightness) * limit, 0.0, limit);

  gl_FragColor = mix(color, vec4(1.0), brightness);
  gl_FragColor.a = unif[5][2];
}
