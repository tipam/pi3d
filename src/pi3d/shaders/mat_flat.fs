#include std_head_fs.inc

void main(void) {
#include std_main_mat.inc
  //if (distance(gl_PointCoord, vec2(0.5)) > 0.5) discard; //circular points
  gl_FragColor = mix(texc, vec4(unif[4], unif[5][1]), ffact); // ------ combine using factors
  gl_FragColor.a *= unif[5][2];
}