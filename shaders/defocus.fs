precision mediump float;

varying vec2 texcoordout;
varying float dist;

uniform sampler2D tex0;
uniform vec3 unif[16];
//uniform float dist_fr => unif[14][0]
//uniform float dist_to => unif[14][1]
//uniform float amount ==> unif[14][2]
//uniform float ix ======> unif[15][0]
//uniform float iy ======> unif[15][1]

void main(void) {
  vec4 texc = vec4(0.0, 0.0, 0.0, 1.0);
  vec2 fcoord = vec2(0.0, 0.0);
  float spread = clamp(unif[14][2] * max((dist-unif[14][0])/(0.0-unif[14][0]), (dist-unif[14][0])/(unif[14][1]-unif[14][0])), 0.0, 1.0);
  float n_samp = 0.0;
  for (float i=-2.0; i < 3.0; i+=1.0) {
    for (float j=-2.0; j < 3.0; j+=1.0) {
      fcoord = (vec2(gl_FragCoord) + vec2(i*spread, j*spread)) * vec2(unif[15]);
      texc.rgb += texture2D(tex0, fcoord).rgb;
      n_samp += 1.0;
    }
  }
  gl_FragColor = texc / n_samp;
}


