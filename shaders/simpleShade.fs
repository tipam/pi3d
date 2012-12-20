precision mediump float;

varying vec3 normout;
varying vec2 texcoordout;
varying vec2 bumpcoordout;
varying mat4 normrot;
varying vec2 shinecoordout;
varying float dist;
varying vec3 lightVector;

uniform sampler2D tex0;
uniform sampler2D tex1;
uniform sampler2D tex2;
uniform mat4 cameraviewmatrix;
uniform vec3 unib[2];
//uniform float blend ====> unib[0][2]


void main(void) {
  vec4 texc = texture2D(tex0, texcoordout); // ------ material or basic colour from texture

  if (true) { // ----- always do this
    float alpha = texc[3];
    if (alpha < unib[0][2]) discard; // ------ to allow rendering behind the transparent parts of this object
    gl_FragColor = texc;
  }
  else {
    vec4 scrap = texture2D(tex1, vec2(0.0, 0.0));
    scrap = texture2D(tex2, vec2(0.0, 0.0));
  }
}



