/////RADIAL BLUR FILTER/////
//www.cloneproduction.net

precision mediump float;
varying vec2 uv;
uniform sampler2D tex0;
uniform sampler2D tex1;

vec2 BlurXY = vec2 (-0.4, -0.0); //blur center position
float Amount = 0.0; //blur radial amount
float BlurR = 0.3; //blur rotation amount

void main(void){
  gl_FragColor = vec4(0.0, 0.0, 0.0, 1.0);
  vec2 piv = vec2(BlurXY.x+0.5, BlurXY.y-0.5);
  float wd = texture2D(tex1,uv).x;
  vec2 d = (uv - piv); // from centre to this pixel
  // use radial vec = -dy, dx
  d = d * Amount / 5.0 + vec2(-d.y, d.x) * BlurR / 5.0;
  for (float i=0.0; i<1.0; i+=0.125){
    gl_FragColor += texture2D(tex0, uv + d * pow(2.0, i)) * 0.125;
  }
}
