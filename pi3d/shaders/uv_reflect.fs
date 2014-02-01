precision mediump float;

varying vec2 texcoordout;
varying vec2 bumpcoordout;
varying vec3 inray;
varying vec3 normout;
varying vec3 lightVector;
varying float dist;

uniform sampler2D tex0;
uniform sampler2D tex1;
uniform sampler2D tex2;
uniform vec3 unib[4];
//uniform float ntiles ===> unib[0][0]
//uniform float shiny ====> unib[0][1]
//uniform vec4 material ==> unib[1]
uniform vec3 unif[16];
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

  float bfact = 1.0 - smoothstep(100.0, 300.0, dist); // ------ for flying
  //float bfact = 1.0 - smoothstep(30.0, 100.0, dist); // ------ attenuate smoothly between 30 and 100 units

  float ffact = smoothstep(unif[5][0]/3.0, unif[5][0], dist); // ------ smoothly increase fog between 1/3 and full fogdist

  float intensity = clamp(dot(lightVector, normalize(vec3(0.0, 0.0, 1.0) + bump * bfact)), 0.0, 1.0); // ------ adjustment of colour according to combined normal
  if (texc.a < unib[0][2]) discard; // ------ to allow rendering behind the transparent parts of this object
  texc.rgb = (texc.rgb * unif[9]) * intensity + (texc.rgb * unif[10]); // ------ directional lightcol * intensity + ambient lightcol

  vec3 refl = reflect(inray, normout + 0.2 * bfact * bump); // ----- reflection direction from this vertex
  vec3 horiz = cross(inray, vec3(0.0, 1.0, 0.0)); // ----- a 'horizontal' unit vector normal to the inray
  vec3 vert = cross(inray, vec3(1.0, 0.0, 0.0)); // ----- a 'vertical' unit vector normal to the inray
  float hval = dot(refl, horiz); // ----- component of the reflected ray along horizonal
  float vval = dot(refl, vert); // -----  componet of reflected ray along vertical
  float zval = dot(refl, -1.0 * inray); // ----- component of reflected ray in direction back to camera
  // ----- now work out the horizonal and vertical angles relative to inray and map them to range 0 to 1
  vec2 shinecoord = vec2(0.5 - atan(hval , zval)/6.283185307, 0.5 - atan(vval , zval)/6.283185307); // ------ potentially need to clamp with bump included in normal
  vec4 shinec = vec4(0.0, 0.0, 0.0, 0.0);
  shinec = texture2D(tex2, shinecoord); // ------ get the reflection for this pixel
  float shinefact = clamp(unib[0][1]*length(shinec)/length(texc), 0.0, unib[0][1]);// ------ reduce the reflection where the ground texture is lighter than it

  gl_FragColor = (1.0 - ffact) * ((1.0 - shinefact) * texc + shinefact * shinec) + ffact * vec4(unif[4], unif[5][1]); // ------ combine using factors
  gl_FragColor.a *= unif[5][2];
}


