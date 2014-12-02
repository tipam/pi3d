#include std_head_fs.inc

varying vec2 bumpcoordout;
varying vec3 inray;
varying vec3 normout;
varying vec3 lightVector;
varying float dist;
varying float lightFactor;

void main(void) {
#include std_main_mat.inc
  vec3 bump = normalize(texture2D(tex0, bumpcoordout).rgb * 2.0 - 1.0);
#include std_bump.inc
#include std_shine.inc
  shinec = texture2D(tex1, shinecoord); // ------ get the reflection for this pixel
  float shinefact = clamp(unib[0][1]*length(shinec)/length(texc), 0.0, unib[0][1]);// ------ reduce the reflection where the ground texture is lighter than it

  gl_FragColor = (1.0 - ffact) * ((1.0 - shinefact) * texc + shinefact * shinec) + ffact * vec4(unif[4], unif[5][1]); // ------ combine using factors
  gl_FragColor.a *= unif[5][2];
}


