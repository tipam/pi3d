#include std_head_fs.inc

varying vec2 texcoordout;
varying vec2 bumpcoordout;
varying vec3 lightVector;
varying float dist;
varying float lightFactor;

varying vec4 shadowposn;

float unpack (vec4 comp)
{
  const vec4 unpackFactors = vec4(1.0 / (256.0 * 256.0), 1.0 / 256.0, 1.0, 0.0);
  //const vec4 unpackFactors = vec4(1.0 / (128.0 * 128.0), 1.0 / 128.0, 1.0, 0.0);
  return dot(comp, unpackFactors);
}

void main(void) {
#include std_main_uv.inc
  vec3 bump = normalize(texture2D(tex1, bumpcoordout).rgb * 2.0 - 1.0);
  bump.y *= -1.0;

  float bfact = 1.0 - smoothstep(100.0, 600.0, dist); // ------ attenuate smoothly between 100 and 600 units

  vec4 normShadow = shadowposn / shadowposn.w;
  normShadow = (normShadow + 1.0) / 2.0;
  vec4 packedZValue = texture2D(tex2, normShadow.st);
  float unpackedZValue = unpack(packedZValue);
  vec2 in_range = step(vec2(0.0), normShadow.st) * (1.0 - step(vec2(1.0), normShadow.st));
  float lightMod = lightFactor * (1.0 -
                  0.9 * step(0.0002, normShadow.z - unpackedZValue) *
                  in_range[0] * in_range[1]);

  float intensity = clamp(dot(lightVector, normalize(vec3(0.0, 0.0, 1.0) + bump * bfact)) * lightMod, 0.0, 1.0); // ------ adjustment of colour according to combined normal
  texc.rgb = (texc.rgb * unif[9]) * intensity + (texc.rgb * unif[10]); // ------ directional lightcol * intensity + ambient lightcol

  gl_FragColor =  (1.0 - ffact) * texc + ffact * vec4(unif[4], unif[5][1]); // ------ combine using factors
  gl_FragColor.a = unif[5][2];
}


