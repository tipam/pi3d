/////COLORIZE FILTER/////
//www.cloneproduction.net

precision mediump float;
varying vec2 uv;
varying vec2 d;
uniform sampler2D tex0;
uniform vec3 unif[20];
//color0 unif[16] in python 48,49,50 = 1.0, 0.5, 0.0 say
//color1 unif[17] in python 51,52,53 = 0.0, 1.0, 0.5 say
//color2 unif[18] in python 54,55,56 = 0.5, 0.0, 1.0 say

void main(void){
  vec4 c1 = texture2D(tex0, uv);     //from sampler
  
  vec3 pixcol = vec3(length(c1.rgb));//each componet equal to brightness
  vec3 tc = vec3 (1.0, 0.0, 0.0);
  vec3 colors[3]; 
  colors[0] = unif[16];
  colors[1] = unif[17];
  colors[2] = unif[18];
  vec3 luma = vec3(0.299, 0.587, 0.114);
  float lum = dot(pixcol, luma);
  float ix = step(0.5, lum);
  tc = mix(colors[0], mix(colors[1], colors[2], ix), (lum - ix * 0.5) / 0.5);
  gl_FragColor = vec4(tc, unif[5][2]);
}
