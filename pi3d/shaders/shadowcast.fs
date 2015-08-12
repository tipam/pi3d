#include std_head_fs.inc

varying vec2 texcoordout;
varying vec4 position;

vec4 pack (float depth)
{
  const vec4 bitSh = vec4(256.0 * 256.0, 256.0, 1.0, 0.0);
  const vec4 bitMsk = vec4(0.0, 1.0 / 256.0, 1.0 / 256.0, 1.0 / 256.0);
  vec4 comp = fract(depth * bitSh);
  comp -= comp.xxyz * bitMsk;
  return comp;
}

void main(void) {
  vec4 texc = texture2D(tex0, texcoordout); // ------ material or basic colour from texture
  if (texc.a < unib[0][2]) discard; // ------ to allow rendering behind the transparent parts of this object
  float normPosn = position.z / position.w;
  normPosn = (normPosn + 1.0) / 2.0;
  gl_FragColor = pack(normPosn);
  gl_FragColor.a = 1.0;
}


