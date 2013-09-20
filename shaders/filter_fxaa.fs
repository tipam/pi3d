/////FAST APPROXIMATE ANTI-ALIASING FILTER/////
//www.cloneproduction.net
//NB This will only work if the mipmap=False setting is used for tex0
//i.e. mypost = pi3d.PostProcess("shader/filter_fxaa", mipmap=False)

precision mediump float;

varying vec2 dNW;
varying vec2 dNE;
varying vec2 dSW;
varying vec2 dSE;
varying vec2 uv;

uniform sampler2D tex0;
uniform vec3 unif[20];

void main( void ) {
  float FXAA_SPAN_MAX = 8.0;
  float FXAA_REDUCE_MUL = 1.0/8.0;
  float FXAA_REDUCE_MIN = 1.0/128.0;

  vec3 rgbNW=texture2D(tex0, uv + dNW).xyz;
  vec3 rgbNE=texture2D(tex0, uv + dNE).xyz;
  vec3 rgbSW=texture2D(tex0, uv + dSW).xyz;
  vec3 rgbSE=texture2D(tex0, uv + dSE).xyz;
  vec3 rgbM=texture2D(tex0, uv).xyz;

  vec3 luma=vec3(0.299, 0.587, 0.114);
  float lumaNW = dot(rgbNW, luma);
  float lumaNE = dot(rgbNE, luma);
  float lumaSW = dot(rgbSW, luma);
  float lumaSE = dot(rgbSE, luma);
  float lumaM  = dot(rgbM,  luma);

  float lumaMin = min(lumaM, min(min(lumaNW, lumaNE), min(lumaSW, lumaSE)));
  float lumaMax = max(lumaM, max(max(lumaNW, lumaNE), max(lumaSW, lumaSE)));

  vec2 dir = vec2(-((lumaNW + lumaNE) - (lumaSW + lumaSE)),
              ((lumaNW + lumaSW) - (lumaNE + lumaSE)));

  float dirReduce = max(
    (lumaNW + lumaNE + lumaSW + lumaSE) * (0.25 * FXAA_REDUCE_MUL),
    FXAA_REDUCE_MIN);


  float rcpDirMin = 1.0/(min(abs(dir.x), abs(dir.y)) + dirReduce);

  dir = min(vec2( FXAA_SPAN_MAX,  FXAA_SPAN_MAX),
      max(vec2(-FXAA_SPAN_MAX, -FXAA_SPAN_MAX),
      dir * rcpDirMin)) / vec2(unif[15][0], unif[15][1]);

  vec3 rgbA = (1.0/2.0) * (
    texture2D(tex0, uv.xy + dir * (1.0/3.0 - 0.5)).xyz +
    texture2D(tex0, uv.xy + dir * (2.0/3.0 - 0.5)).xyz);
  vec3 rgbB = rgbA * (1.0/2.0) + (1.0/4.0) * (
    texture2D(tex0, uv.xy + dir * (0.0/3.0 - 0.5)).xyz +
    texture2D(tex0, uv.xy + dir * (3.0/3.0 - 0.5)).xyz);
  float lumaB = dot(rgbB, luma);
  
  gl_FragColor= vec4(lumaB, lumaB, lumaB, unif[5][2]);

  if ((lumaB < lumaMin) || (lumaB > lumaMax)){
    gl_FragColor.xyz = rgbA;
  } else {
    gl_FragColor.xyz = rgbB;
  }
}
