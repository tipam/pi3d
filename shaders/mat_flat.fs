precision mediump float;

varying float dist;

uniform vec3 unib[4];
//uniform vec4 material ==> unib[1]
uniform vec3 unif[16];
//uniform vec3 fogshade ==> unif[4]
//uniform float fogdist ==> unif[5][0]
//uniform float fogalpha => unif[5][1]

void main(void) {
  //if (distance(gl_PointCoord, vec2(0.5)) > 0.5) discard; //circular points
  float ffact = smoothstep(unif[5][0]/3.0, unif[5][0], dist); // ------ smoothly increase fog between 1/3 and full fogdist
  vec4 texc = vec4(unib[1], 1.0); // ------ basic colour from material vector
  gl_FragColor = (1.0 - ffact) * texc + ffact * vec4(unif[4], unif[5][1]); // ------ combine using factors
  gl_FragColor.a *= unif[5][2];
}


