#include std_head_fs.inc

varying vec3 lightVector;
varying float dist;
varying float lightFactor;

void main(void) {
#include std_main_mat.inc
#include std_light.inc

  gl_FragColor =  (1.0 - ffact) * texc + ffact * vec4(unif[4], unif[5][1]); // ------ combine using factors
  gl_FragColor.a *= unif[5][2];
}


