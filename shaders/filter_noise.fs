/////NOISE FILTER/////
//http://pixelshaders.com

precision lowp float;

varying vec2 uv;

uniform sampler2D tex0;
uniform vec3 unif[20];
// time unif[16][0]
// scale unif[16][1]
// limit unif[16][2]

float t = unif[16][0];
float scale = unif[16][1];
float limit = unif[16][2];
float r[10];

float noise(vec2 p) {
  return fract(sin(p.x + p.y * 10000.0) * 10000.0);
}

float smoothNoise(vec2 p) {
  vec2 inter = fract(p);
  float s = mix(noise(vec2(floor(p.x), floor(p.y))),
                noise(vec2(ceil(p.x), floor(p.y))), inter.x);
  float n = mix(noise(vec2(floor(p.x), ceil(p.y))),
                noise(vec2(ceil(p.x), ceil(p.y))), inter.x);
  return mix(s, n, inter.y);
}

float movingNoise(vec2 p) {
  float total =   smoothNoise(p - t) +
                  smoothNoise(p*2.0 + t) * 0.5 +
                  smoothNoise(p*4.0 - t) * 0.25 +
                  smoothNoise(p*8.0 + t) * 0.125;
                  smoothNoise(p*16.0 - t) * 0.0625;
  total *= 0.516129032; // i.e. 1.0 / (1.0 + 0.5 + 0.25 + 0.125 + 0.0625)
  // reduce or increase the number octaves to change effect and speed
  //total *= 0.533333333;
  return total;
}

float nestedNoise(vec2 p) {
  float x = movingNoise(p);
  float y = movingNoise(p + 20.0);
  return movingNoise(p + vec2(x, y));
}

void main(void) { 
  vec4 color = texture2D(tex0, uv);
  
  vec2 p = uv * 6.0;
  float brightness = nestedNoise(p);

  gl_FragColor = mix(color, vec4(1.0), brightness);
  gl_FragColor.a = unif[5][2];
}
