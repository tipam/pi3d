#include std_head_fs.inc

varying vec2 texcoordout;
varying vec2 bumpcoordout;
varying vec3 inray;
varying vec3 normout;
varying vec3 lightVector;
varying float lightFactor;

void main(void) {
#include std_main_uv.inc
  vec3 bump = normalize(texture2D(tex1, bumpcoordout).rgb * 2.0 - 1.0);
#include std_bump.inc
#include std_shine.inc
  shinec = texture2D(tex2, shinecoord); // ------ get the reflection for this pixel
  shinec += vec4(max(pow(dot(refl, -inray), 4.0), 0.0) * unib[4], 1.0); // Phong specular
  float shinefact = clamp(unib[0][1]*length(shinec)/length(texc), 0.0, unib[0][1]);// ------ reduce the reflection where the ground texture is lighter than it

  gl_FragColor = mix(mix(texc, shinec, shinefact), vec4(unif[4], unif[5][1]), ffact); // ------ combine using factors
  gl_FragColor.a *= unif[5][2];
}