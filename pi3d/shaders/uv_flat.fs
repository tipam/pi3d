#include std_head_fs.inc

varying vec2 texcoordout;

void main(void) {
#include std_main_uv.inc
  gl_FragColor = mix(texc, vec4(unif[4], unif[5][1]), ffact); // ------ combine using factors
  gl_FragColor.a *= unif[5][2];
}