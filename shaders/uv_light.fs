precision mediump float;

varying vec3 normout;
varying vec2 texcoordout;
varying vec3 lightVector;
varying float dist;

uniform sampler2D tex0;
uniform vec3 unib[2];
//uniform float blend ====> unib[0][2]
uniform vec3 unif[11];
//uniform vec3 fogshade ==> unif[4]
//uniform float fogdist ==> unif[5][0]
//uniform float fogalpha => unif[5][1]

void main(void) {
  vec4 texc = texture2D(tex0, texcoordout); // ------ basic colour from texture

  float ffact = smoothstep(unif[5][0]/3.0, unif[5][0], dist); // ------ smoothly increase fog between 1/3 and full fogdist
  float intensity = max(dot(lightVector, normout), 0.1); // ------ adjustment of colour according to combined normal
  float alpha = texc[3];
  if (alpha < unib[0][2]) discard; // ------ to allow rendering behind the transparent parts of this object
  texc = texc * intensity;
  texc[3] = alpha; // ------ the alpha value from before darkening is patched back in, otherwise dark things might become see through
  gl_FragColor =  (1.0 - ffact) * texc + ffact * vec4(unif[4], unif[5][1]); // ------ combine using factors
}


