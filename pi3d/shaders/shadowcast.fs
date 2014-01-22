precision mediump float;

varying vec2 texcoordout;
varying vec2 bumpcoordout;
varying vec3 lightVector;
varying float dist;
varying vec2 shadcoordout;

uniform sampler2D tex0;
uniform sampler2D tex1;
uniform sampler2D tex2;
uniform vec3 unib[4];
//uniform float ntiles ===> unib[0][0]
//uniform float shiny ====> unib[0][1]
//uniform vec4 material ==> unib[1]
uniform vec3 unif[20];
//uniform vec3 fogshade ==> unif[4]
//uniform float fogdist ==> unif[5][0]
//uniform float fogalpha => unif[5][1]
//uniform vec3 lightcol => unif[9]
//uniform vec3 lightamb => unif[10]

void main(void) {
  vec4 texc = texture2D(tex0, texcoordout); // ------ basic colour from texture

  // ------ look up normal map value as a vector where each colour goes from -100% to +100% over its range so
  // ------ 0xFF7F7F is pointing right and 0X007F7F is pointing left. This vector is then rotated relative to the rotation
  // ------ of the normal at that vertex.
  vec3 bump = normalize(texture2D(tex1, bumpcoordout).rgb * 2.0 - 1.0);
  bump.y *= -1.0;

  float bfact = 1.0 - smoothstep(30.0, 100.0, dist); // ------ attenuate smoothly between 30 and 100 units

  float ffact = smoothstep(unif[5][0]/3.0, unif[5][0], dist); // ------ smoothly increase fog between 1/3 and full fogdist
  
  float sfact = 1.0 - 0.4 * smoothstep(0.05, 0.25, length(texture2D(tex2, shadcoordout))); // ------ half light where shadecoord > 0.9
  //float sfact = 1.0 - 0.5 * step(0.01, length(texture2D(tex2, shadcoordout)));

  float intensity = sfact * clamp(dot(lightVector, normalize(vec3(0.0, 0.0, 1.0) + bump * bfact)), 0.0, 1.0); // ------ adjustment of colour according to combined normal
  if (texc.a < unib[0][2]) discard; // ------ to allow rendering behind the transparent parts of this object
  texc.rgb = (texc.rgb * unif[9]) * intensity + (texc.rgb * unif[10]); // ------ directional lightcol * intensity + ambient lightcol

  gl_FragColor =  (1.0 - ffact) * texc + ffact * vec4(unif[4], unif[5][1]); // ------ combine using factors
  gl_FragColor.a *= unif[5][2];
}


