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

float taper(float x, float from, float to, float nVal) {
  float fVal = 1.0 - nVal;
  if (x < from) return nVal;
  else if (x > to) return fVal;
  else return nVal + (x - from)/(to - from)*(fVal-nVal);
}

void main(void) {
  vec3 lightVector = normalize(vec3 (cameraviewmatrix * vec4(lightpos,0.0)));
  vec3 bump;
  bump = vec3(0.0, 0.0, 0.0);
  if (ntiles > 0.0) bump = vec3(normrot * vec4(normalize(texture2D(tex1, bumpcoordout)).rgb * 2.0 - 1.0, 0.0));
  float bfact = taper(dist, 20.0, 75.0, 1.0);

  float ffact = 0.0;
  if (fogdist != 0.0) ffact = taper(dist, fogdist/3.0, fogdist, 0.0);

  float intensity = max(dot(lightVector, normout + bump * bfact), 0.0);
  vec4 texc = texture2D(tex0, texcoordout) * intensity;
  vec4 shinec = vec4(0.0, 0.0, 0.0, 0.0);
  if (shiny > 0.0) shinec = texture2D(tex2, shinecoordout);
  float shinefact = shiny;
  if (length(shinec) < length(texc)) shinefact *= 0.25;
  
  gl_FragColor = (1.0 - ffact) * ((1.0 - shinefact) * texc + shinefact * shinec) + ffact * fogshade;
}
