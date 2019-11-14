#include std_head_fs.inc

varying vec2 texcoordout;
varying vec2 bumpcoordout;
varying vec3 lightVector;
varying vec3 normout;
varying vec3 inray;
varying float lightFactor;

void main(void) {
  float ffact = smoothstep(unif[5][0]/3.0, unif[5][0], dist); // ------ smoothly increase fog between 1/3 and full fogdist
  vec4 texc = vec4(0.0, 0.0, 0.0, 1.0);
  if (abs(dot(normout, inray)) > 0.1) {
    texc = texture2D(tex0, texcoordout); // ------ basic colour from texture

    vec3 bump = normalize(texture2D(tex1, bumpcoordout).rgb * 2.0 - 1.0);
    bump.y *= -1.0;

    float bfact = 1.0 - smoothstep(30.0, 100.0, dist); // ------ attenuate smoothly between 30 and 100 units

    float intensity = clamp(dot(lightVector, normalize(vec3(0.0, 0.0, 1.0) + bump * bfact)) * lightFactor, 0.0, 1.0); // ------ adjustment of colour according to combined normal
    if (texc.a < unib[0][2]) discard; // ------ to allow rendering behind the transparent parts of this object
    texc.rgb = (texc.rgb * unif[9]) * intensity + (texc.rgb * unif[10]); // ------ directional lightcol * intensity + ambient lightcol

    float d = 5.0;
    float r = length(texc.rgb) * 0.6;
    float fact = 3.141 * pow(r, 2.0);
    r *= d;

    vec2 dcentre = floor(gl_FragCoord.xy / d + 0.5) * d;
    float dist = 0.5 * distance(gl_FragCoord.xy, dcentre);
    if (r > dist) fact = 2.0;
    texc.rgb = (texc.rgb - 1.0 + fact) / fact;
  }
  gl_FragColor = mix(texc, vec4(unif[4], unif[5][1]), ffact); // ------ combine using factors
  gl_FragColor = floor(gl_FragColor * 8.0 + 0.5) / 8.0;
  gl_FragColor.a *= unif[5][2];
}


