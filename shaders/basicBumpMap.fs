varying vec2 texcoordout;
uniform sampler2D tex0;
uniform sampler2D normalmap;
uniform vec3 lightpos;

void main(void) {
  vec3 lightVector = normalize(lightpos);
  vec3 norm = normalize(texture2D(normalmap, texcoordout).rgb * 2.0 - 1.0);
  float intensity = max(dot(norm,lightVector), 0.0);
  vec3 colour = texture2D(tex0, texcoordout).rgb * intensity; 
  gl_FragColor = vec4(colour, 1.0);
}
