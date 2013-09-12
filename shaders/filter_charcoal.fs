/////CHARCOAL FILTER/////
//www.cloneproduction.net

precision mediump float;
varying vec2 uv;
varying vec2 d;
uniform sampler2D tex0;

void main(void){
  vec4 c1 = texture2D(tex0, uv);
  //attempt to stop 'wrapping'
  vec4 c2 = texture2D(tex0, uv + vec2(clamp(d.x, 0.0, 1.0), 0));
  vec4 c3 = texture2D(tex0, uv + vec2(0, clamp(d.y, -1.0, 0.0)));
  float f = distance(c1.rgb, c2.rgb) + distance(c1.rgb, c3.rgb) - 0.2;
  f = clamp(f, 0.0, 1.0);
  c1.rgb = vec3(1.0, 1.0, 1.0) * (1.0 - f);
  gl_FragColor = c1;
}
