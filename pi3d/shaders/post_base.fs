#include std_head_fs.inc

varying vec2 texcoordout;

void main(void) {
  ///////////////////////////////////////////////////////////////////
  // you can do processing on the texture (or utilise other textures)
  // here. This skeleton just does a fairly approximate convolution
  // with a variable offset distance
  ///////////////////////////////////////////////////////////////////
  vec4 texc = vec4(0.0, 0.0, 0.0, 1.0);

  float dx[9]; // x offsets
  float dy[9]; // y offsets
  float f[9];  // factors. NB the book says that arrays can be initialized
  // float x[3] = float[](1.0, 1.0, 1.0); but I can't get it to work
  dx[0] = -0.00125; dx[1] = 0.0; dx[2] = 0.00125;
  dx[3] = -0.00125; dx[4] = 0.0; dx[5] = 0.00125;
  dx[6] = -0.00125; dx[7] = 0.0; dx[8] = 0.00125;
  
  dy[0] =  0.00125; dy[1] =  0.00125; dy[2] =  0.00125;
  dy[3] =  0.0;     dy[4] =  0.0;     dy[5] =  0.0;
  dy[6] = -0.00125; dy[7] = -0.00125; dy[8] = -0.00125;
  
  f[0] =  0.75; f[1] = -1.0;  f[2] =  0.75;
  f[3] = -1.0;  f[4] =  1.1;  f[5] = -1.0;
  f[6] =  0.75; f[7] = -1.0;  f[8] =  0.75;
  
  vec2 fcoord = vec2(0.0, 0.0);
  
  for (int i=0; i<9; i+=1) {
    fcoord = (texcoordout + vec2(dx[i] * unif[16][0], dy[i] * unif[16][0]));
    texc += (texture2D(tex0, fcoord) * f[i]);
  }
  
  gl_FragColor = texc;
}


