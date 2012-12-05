precision highp float;

attribute vec3 vertex;
attribute vec3 normal;
attribute vec2 texcoord;

uniform mat4 modelviewmatrix;
uniform mat4 cameraviewmatrix;
uniform float ntiles;
uniform float shiny;
uniform vec3 locn;
uniform vec3 rotn;
uniform vec3 scle;
uniform vec3 ofst;
uniform vec3 eye;

varying vec3 normout;
varying vec2 texcoordout;
varying vec2 bumpcoordout;
varying mat4 normrot;
varying vec2 shinecoordout;
varying float dist;

mat4 transpose(mat4 m) {
  mat4 o;
  for (int j=0; j<4; j++)
    for (int i=0; i<4; i++) o[i][j] = m[j][i];
  return o;
}

void main(void) {
  
  float s, c;
  mat4 newmodel = cameraviewmatrix;
  
  newmodel = mat4(
    1.0,0.0,0.0,0.0, 
    0.0,1.0,0.0,0.0, 
    0.0,0.0,1.0,0.0, 
    (locn.x-ofst.x),(locn.y-ofst.y),(locn.z-ofst.z),1.0) * newmodel;
  //newmodel = transpose(newmodel);
  /*
  if (rotn.z != 0.0) {
    s = sin(radians(rotn.z));
    c = cos(radians(rotn.z));
    newmodel = mat4(c,s,0.0,0.0, -s,c,0.0,0.0, 0.0,0.0,1.0,0.0, 0.0,0.0,0.0,1.0) * newmodel; } 
  */
  /*
  if (rotn.y != 0.0) {
    s = sin(radians(rotn.y));
    c = cos(radians(rotn.y));
    newmodel = mat4(c,0.0,-s,0.0, 0.0,1.0,0.0,0.0, s,0.0,c,0.0, 0.0,0.0,0.0,1.0) * newmodel; } 
  */
  /*
  if (rotn.x != 0.0) {
    s = sin(radians(rotn.x));
    c = cos(radians(rotn.x));
    newmodel = mat4(1.0,0.0,0.0,0.0, 0.0,c,s,0.0, 0.0,-s,c,0.0, 0.0,0.0,0.0,1.0) * newmodel; } 
  */
  /*
  if (scle.x > 0.0 && scle.y > 0.0 && scle.z > 0.0)
    newmodel = mat4(scle.x,0.0,0.0,0.0, 0.0,scle.y,0.0,0.0, 0.0,0.0,scle.z,0.0, 0.0,0.0,0.0,1.0) * newmodel;
  */
  
  //newmodel = transpose(newmodel);
  
  
  newmodel = mat4(
    1.0,0.0,0.0,0.0, 
    0.0,1.0,0.0,0.0, 
    0.0,0.0,1.0,0.0, 
    ofst.x,ofst.y,ofst.z,1.0) * newmodel;
  

  normout = vec3(newmodel * vec4(normal,0.0));
  if (length(normout) > 0.0) normout = normalize(normout);
  
  if (ntiles == 0.0) { // ntiles doubles as flag for normal mapping
    bumpcoordout = texcoord;
    normrot = mat4(1.0);
  }
  else {
    vec3 bnorm = vec3(0,0,-1.0); // normal to original bump map sheet
    float c = dot(bnorm, normout); // cos
    float t = 1.0 - c;
    vec3 a = cross(bnorm, normout); // axis
    float s = length(a); // sine (depends on bnorm and normout being unit)
    if (s > 0.0) a = normalize(a);
    normrot = mat4(
      t * a.x * a.x + c, t * a.x * a.y + a.z * s, t * a.x * a.z - a.y * s, 0.0,
      t * a.x * a.y - a.z * s, t * a.y * a.y + c, t * a.z * a.y + a.x * s, 0.0,
      t * a.x * a.z + a.y * s, t * a.y * a.z - a.x * s, t * a.z * a.z + c, 0.0,
      0.0, 0.0, 0.0, 1.0);
    bumpcoordout = texcoord * ntiles;
  }
  
  if (shiny == 0.0) {
    shinecoordout = vec2(0.0, 0.0);
  }
  else {
    vec3 inray = vertex - vec3(newmodel * vec4(eye, 1.0));
    if (length(inray) > 0.0) inray = normalize(inray);
    vec3 refl = reflect(inray, normout);
    vec3 horiz = cross(inray, vec3(0.0, 1.0, 0.0));
    vec3 vert = cross(inray, vec3(1.0, 0.0, 0.0));
    float hval = dot(refl, horiz);
    float vval = dot(refl, vert);
    float zval = dot(refl, inray);
    shinecoordout = vec2(max(0.0, 0.5 + atan(hval, zval)/3.14159265), min(1.0, 0.5 + atan(vval, zval)/3.14159265));
  }
  vec4 relPosn = newmodel * vec4(vertex,1.0);
  dist = length(relPosn);
  texcoordout = texcoord;
  gl_Position = relPosn;
}
