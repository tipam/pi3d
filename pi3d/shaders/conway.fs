precision mediump float;

uniform sampler2D tex0;
uniform vec3 unib[4];
//uniform float blend ====> unib[0][2]
uniform vec3 unif[20];
//uniform vec2 (x, y) =========> unif[14]
//uniform vec3(w, h, full_h) => unif[15]

varying vec2 pix_inv;

void main(void) {
  vec2 coord = vec2(gl_FragCoord); //pixel position
  vec2 fcoord = vec2(0.0, 0.0); //to hold 0 to 1.0 image coordinates see pix_inv below
  float ntot = 0.0; //total score of 3x3 grid of pixels
  for (float i=-1.0; i < 2.0; i+=1.0) {
    for (float j=-1.0; j < 2.0; j+=1.0) {
      fcoord = (coord + vec2(i, j)) * pix_inv; // really dividing to scale 0-1 i.e. (x/w, y/h)
      ntot += step(0.25,(texture2D(tex0, fcoord)).b); //add 1.0 if blue > 0.25
    }
  }
  vec4 texc = texture2D(tex0, (coord * pix_inv)); //current value of pixel
  ntot -= step(0.25, texc.b); // take away this square (centre of grid)
  if (ntot == 3.0) texc = vec4(0.0, 0.0, 1.0, 1.0);
  else if (ntot != 2.0) texc = vec4(smoothstep(0.0, 5.0, ntot), 1.0, 0.0, 0.0);
  gl_FragColor = texc;
  gl_FragColor.a = 1.0;
}
