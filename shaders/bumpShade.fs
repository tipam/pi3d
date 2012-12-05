precision mediump float;

varying vec3 normout;
varying vec2 texcoordout;
varying vec2 bumpcoordout;
varying mat4 normrot;
varying vec2 shinecoordout;
varying float dist;

uniform sampler2D tex0;
uniform sampler2D tex1;
uniform sampler2D tex2;
uniform vec3 lightpos;
uniform mat4 cameraviewmatrix;
uniform float ntiles;
uniform float shiny;
uniform float fogdist;
uniform vec4 fogshade;
uniform float blend;
uniform vec4 material;

void main(void) {
  vec4 texc = material;
  if (material == vec4(0.0, 0.0, 0.0, 0.0)) texc = texture2D(tex0, texcoordout); // ------ material or basic colour from texture

  if (shiny < 0.0) { // ------ don't have shadows i.e. for sprites or environment cubes
    float alpha = texc[3];
    if (alpha < blend) discard; // ------ to allow rendering behind the transparent parts of this object
    gl_FragColor = texc;
  }
  else {
    vec3 lightVector = normalize(vec3 (cameraviewmatrix * vec4(lightpos, 0.0))); // ------ rotate relative to view
    vec3 bump;
    bump = vec3(0.0, 0.0, 0.0);
    // ------ look up normal map value as a vector where each colour goes from -100% to +100% over its range so
    // ------ 0xFF7F7F is pointing right and 0X007F7F is pointing left. This vector is then rotated relative to the rotation
    // ------ of the normal at that vertex.
    if (ntiles > 0.0) bump = vec3(normrot * vec4(normalize(texture2D(tex1, bumpcoordout)).rgb * 2.0 - vec3(1.0, 1.0, 1.0), 0.0));
    float bfact = 1.0 - smoothstep(20.0, 75.0, dist); // ------ attenuate smoothly between 20 and 75 units

    float ffact = 0.0;
    if (fogdist != 0.0) ffact = smoothstep(fogdist/3.0, fogdist, dist); // ------ smoothly increase fog between 1/3 and full fogdist

    float intensity = max(dot(lightVector, normout + bump * bfact), 0.1); // ------ adjustment of colour according to combined normal
    float alpha = texc[3];
    if (alpha < blend) discard; // ------ to allow rendering behind the transparent parts of this object
    texc = texc * intensity;
    texc[3] = alpha; // ------ the alpha value from before darkening is patched back in, otherwise dark things might become see through
    vec4 shinec = vec4(0.0, 0.0, 0.0, 0.0);
    if (shiny > 0.0) shinec = texture2D(tex2, shinecoordout); // ------ get the reflection for this pixel
    float shinefact = shiny;
    if (length(shinec) < length(texc)) shinefact *= 0.25; // ------ reduce the reflection where the ground texture is lighter than it
    gl_FragColor = (1.0 - ffact) * ((1.0 - shinefact) * texc + shinefact * shinec) + ffact * fogshade; // ------ combine using factors
  }
}


