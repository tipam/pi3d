precision mediump float;

varying vec3 normout;
varying vec2 texcoordout;
uniform sampler2D tex0;
uniform vec3 lightpos;

void main(void) {
  vec3 lightVector = normalize(lightpos);
  vec3 norm = normalize(normout);
  float intensity = max(dot(lightVector, norm), 0.2);
  gl_FragColor = texture2D(tex0, texcoordout) * intensity;
}
