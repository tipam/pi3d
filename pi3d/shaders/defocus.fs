#include std_head_fs.inc

varying float dist;

void main(void) {
  vec4 texc = vec4(0.0, 0.0, 0.0, 1.0); // we don't save the alpha value of the rendering so set this here to 1.0
  vec2 fcoord = vec2(0.0, 0.0);
  // because the for loops cant run over variable size we have to use a 5 x 5 grid and vary the spread that is sampled
  // obviously this will lead to grainy effects with large amounts of blur
  float spread = clamp(unif[14][2] * max((dist-unif[14][0])/(0.0-unif[14][0]), (dist-unif[14][0])/(unif[14][1]-unif[14][0])), 0.0, unif[14][2]);
  for (float i=-2.0; i < 3.0; i+=1.0) {
    for (float j=-2.0; j < 3.0; j+=1.0) {
      fcoord = (vec2(gl_FragCoord) + vec2(i*spread, j*spread)) * vec2(unif[15]);
      texc.rgb += texture2D(tex0, fcoord).rgb;
    }
  }
  gl_FragColor = texc * 0.04;
  gl_FragColor.a = unif[5][2];
}


