#include std_head_fs.inc

uniform sampler2D tex3;
uniform sampler2D tex4;
uniform sampler2D tex5;
uniform sampler2D tex6;
uniform sampler2D tex7;

varying vec2 texcoordout;
varying vec2 bumpcoordout;
varying vec3 lightVector;
varying float lightFactor;
varying float texFactor;

void main(void) {
  vec4 texc = mix(
                  mix(texture2D(tex0, texcoordout), texture2D(tex2, texcoordout), clamp(texFactor, 0.0, 1.0)),
                  mix(texture2D(tex4, texcoordout), texture2D(tex6, texcoordout), clamp((texFactor - 2.0), 0.0, 1.0)),
                  clamp((texFactor - 1.0), 0.0, 1.0));
  texc.rgb += unib[1] - vec3(0.5);
  float ffact = smoothstep(unif[5][0]/3.0, unif[5][0], dist); // ------ smoothly increase fog between 1/3 and full fogdist
  vec3 bump = normalize(mix(
                  mix(texture2D(tex1, bumpcoordout), texture2D(tex3, bumpcoordout), clamp(texFactor, 0.0, 1.0)),
                  mix(texture2D(tex5, bumpcoordout), texture2D(tex7, bumpcoordout), clamp((texFactor - 2.0), 0.0, 1.0)),
                  clamp((texFactor - 1.0), 0.0, 1.0)).rgb * 2.0 - 1.0);
#include std_bump.inc

  gl_FragColor = mix(texc, vec4(unif[4], unif[5][1]), ffact); // ------ combine using factors
  gl_FragColor.a *= unif[5][2];
}