precision mediump float;

varying vec2 texcoordout;
varying float dist;

uniform sampler2D tex0;

void main(void) {
  vec4 texc = texture2D(tex0, texcoordout); // ------ material or basic colour from texture
  if (dist > 2.5 || texc.a < 0.6) discard; // ------ only render near, non-transparent parts of objects
  gl_FragColor = texc;
}
