#include std_head_fs.inc

varying vec2 texcoordout;
varying vec2 bumpcoordout;
varying vec3 lightVector;
varying float lightFactor;

void main(void) {
 #include std_main_uv.inc
  vec3 bump = normalize(texture2D(tex1, bumpcoordout).rgb * 2.0 - 1.0);
#include std_bump.inc

  gl_FragColor = mix(texc, vec4(unif[4], unif[5][1]), ffact); // ------ combine using factors
  gl_FragColor.a *= unif[5][2];
}