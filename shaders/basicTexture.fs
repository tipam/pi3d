
varying vec2 texcoordout;
uniform sampler2D tex0;

void main(void) {
  gl_FragColor = texture2D(tex0, texcoordout);
}
