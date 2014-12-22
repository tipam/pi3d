#include std_head_fs.inc

varying vec2 pix_inv;

void main(void) {
  vec2 coord = vec2(gl_FragCoord);
  //coord.y += 0.5;
  //coord.x += 0.5;
  coord.y = unif[15][2] - coord.y; // top left convension though means flipping image!
  if (coord.x <= unif[14][0] || coord.x > unif[14][0]+unif[15][0] ||
      coord.y <= unif[14][1] || coord.y > unif[14][1]+unif[15][1]) discard; // only draw the image once
  coord -= unif[14].xy; // offset
  coord *=  pix_inv; // really dividing to scale 0-1 i.e. (x/w, y/h)
  vec4 texc = texture2D(tex0, coord);
  if (texc.a < unib[0][2]) discard; // ------ to allow rendering behind the transparent parts of this object
  gl_FragColor = texc;
  gl_FragColor.a *= unif[5][2];
}


