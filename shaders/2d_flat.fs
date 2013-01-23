precision highp float;

uniform sampler2D tex0;
uniform vec3 unif[16];
//uniform vec2 (x, y) =========> unif[14]
//uniform vec2 (w, h, full_h) => unif[15]

varying vec2 pix_inv;

void main(void) {
  vec2 coord = vec2(gl_FragCoord);
  //coord.y += 0.5;
  //coord.x += 0.5;
  coord.y = unif[15][2] - coord.y; // top left convension though means flipping image!
  if (coord.x <= unif[14][0] || coord.x > unif[14][0]+unif[15][0] ||
      coord.y <= unif[14][1] || coord.y > unif[14][1]+unif[15][1]) discard; // only draw the image once
  coord -= unif[14].xy;
  coord *=  pix_inv;
  gl_FragColor = texture2D(tex0, coord);
}


