precision mediump float;

varying vec3 normout;
varying vec3 lightVector;
varying float dist;

uniform vec3 unib[2];
//uniform vec4 material ==> unib[1]
uniform vec3 unif[11];
//uniform vec3 fogshade ==> unif[4]
//uniform float fogdist ==> unif[5][0]
//uniform float fogalpha => unif[5][1]

void main(void) {
  vec4 texc = vec4(unib[1], 1.0); // ------ basic colour from material vector

  float ffact = smoothstep(unif[5][0]/3.0, unif[5][0], dist); // ------ smoothly increase fog between 1/3 and full fogdist
  float intensity = max(dot(lightVector, normout), 0.1); // ------ adjustment of colour according to combined normal
  texc.rgb = texc.rgb * intensity;
  gl_FragColor =  (1.0 - ffact) * texc + ffact * vec4(unif[4], unif[5][1]); // ------ combine using factors
}

