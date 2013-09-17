/////CHARCOAL FILTER/////
//www.cloneproduction.net

precision mediump float;
varying vec2 uv;
varying vec2 d;
uniform sampler2D tex0;
uniform vec3 unif[20];
// charcoal color unif[16] in python unif 48,49,50
// paper color unif[17] in python unif 51, 52, 53

vec3 charcoal = unif[16];
vec3 paper = unif[17];

void main(void){
  vec4 c1 = texture2D(tex0, uv);
  //attempt to stop 'wrapping'
  vec4 c2 = texture2D(tex0, uv + vec2(clamp(d.x, 0.0, 1.0), 0));
  vec4 c3 = texture2D(tex0, uv + vec2(0, clamp(d.y, -1.0, 0.0)));
  float f = distance(c1.rgb, c2.rgb) + distance(c1.rgb, c3.rgb) - 0.2;
  f = clamp(f, 0.0, 1.0);
  c1.rgb = mix(paper, charcoal, f);
  gl_FragColor = c1;
  gl_FragColor.a *= unif[5][2];
}
