/////SEPIA FILTER/////
//www.cloneproduction.net

precision mediump float;
varying vec2 uv;
uniform sampler2D tex0;
uniform vec3 unif[20];

float viInner = 0.0; //vignette gradient inner
float viOuter = 1.0; //vignette gradient outer

void main(void){
  vec4 c = texture2D(tex0, uv);
  float dist = distance(uv, vec2(0.5, 0.5));
  float vignette = smoothstep(viOuter, viInner, dist);
  gl_FragColor.r = dot(c.rgb, vec3(0.393, 0.769, 0.189))*vignette;
  gl_FragColor.g = dot(c.rgb, vec3(0.349, 0.686, 0.168))*vignette;
  gl_FragColor.b = dot(c.rgb, vec3(0.272, 0.534, 0.131))*vignette;
  gl_FragColor.a = c.a * unif[5][2];
;
}
