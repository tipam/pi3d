/////LENS DISTORTION FILTER/////
//www.cloneproduction.net

precision mediump float;

varying vec2 uv;

uniform sampler2D tex0;
uniform vec3 unif[20];
//lens centre x ==> unif[16][0]
//lens centre y ==> unif[16][1]
//lens radius ==> unif[16][2]

vec2 centre = vec2(unif[16]);
float radius = unif[16][2];
float mag_inv = 0.95; // 1.0/magnification

void main(void) {
  vec2 c = vec2(centre.x + 0.5, centre.y + 0.5);
  vec2 offset = uv - c;
  float x = length(offset) / radius;
  float y = clamp(mag_inv * x + (1.0 - mag_inv) * pow(x, 2.0), 0.0, 1.0);
  gl_FragColor = texture2D(tex0, c + offset * y);
  gl_FragColor.a = unif[5][2];
}


