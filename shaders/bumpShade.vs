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
uniform vec3 rtn;
uniform vec3 lightpos;

varying vec3 normout;
varying vec2 texcoordout;
varying vec2 bumpcoordout;
varying mat4 normrot;
varying vec2 shinecoordout;
varying float dist;
varying vec3 lightVector;

mat4 transpose(mat4 mi) {
  mat4 mo = mat4(0.0);
  for (int i=0; i<4; i++) for (int j=0; j<4; j++) mo[i][j] = mi[j][i];
  return mo;
  }

void main(void) {
  
  float s, c;
  lightVector = normalize(vec3(cameraviewmatrix * vec4(lightpos, 0.0)));
  /*
  lightVector = lightpos;

  s = sin(radians(rtn.y));
  c = cos(radians(rtn.y));
  lightVector = mat3(c,0.0,-s, 0.0,1.0,0.0, s,0.0,c) * lightVector;
  s = sin(radians(rtn.x));
  c = cos(radians(rtn.x));
  lightVector = mat3(1.0,0.0,0.0, 0.0,c,s, 0.0,-s,c) * lightVector;
  */
  mat4 newmodel = transpose(cameraviewmatrix);

  newmodel = mat4(
    1.0, 0.0, 0.0, (locn.x-ofst.x), 
    0.0,1.0,0.0,(locn.y-ofst.y), 
    0.0,0.0,1.0,(locn.z-ofst.z), 
    0.0,0.0,0.0,1.0) * newmodel;

  if (rotn.z != 0.0) {
    s = sin(radians(rotn.z));
    c = cos(radians(rotn.z));
    newmodel = mat4(c,-s,0.0,0.0, s,c,0.0,0.0, 0.0,0.0,1.0,0.0, 0.0,0.0,0.0,1.0) * newmodel; 
  } 
  
  
  if (rotn.x != 0.0) {
    s = sin(radians(rotn.x));
    c = cos(radians(rotn.x));
    newmodel = mat4(1.0,0.0,0.0,0.0, 0.0,c,-s,0.0, 0.0,s,c,0.0, 0.0,0.0,0.0,1.0) * newmodel; 
  } 
  

  if (rotn.y != 0.0) {
    s = sin(radians(rotn.y));
    c = cos(radians(rotn.y));
    newmodel = mat4(c,0.0,s,0.0, 0.0,1.0,0.0,0.0, -s,0.0,c,0.0, 0.0,0.0,0.0,1.0) * newmodel; 
  } 
  
  
  if (scle.x > 0.0 && scle.y > 0.0 && scle.z > 0.0)
    newmodel = mat4(scle.x,0.0,0.0,0.0, 0.0,scle.y,0.0,0.0, 0.0,0.0,scle.z,0.0, 0.0,0.0,0.0,1.0) * newmodel;
    
  newmodel = mat4(
    1.0,0.0,0.0,ofst.x, 
    0.0,1.0,0.0,ofst.y, 
    0.0,0.0,1.0,ofst.z, 
    0.0,0.0,0.0,1.0) * newmodel;

  mat4 newmodel_t = transpose(newmodel);
  ///////////////////////////////////////////////////////////////////////////////

  normout = normalize(vec3(newmodel_t * vec4(normal, 0.0)));
  
  if (ntiles == 0.0) { // ----- ntiles doubles as flag for normal mapping
    bumpcoordout = texcoord;
    normrot = mat4(1.0);
  }
  else {
    vec3 bnorm = vec3(0.0, 0.0, 1.0); // ----- normal to original bump map sheet
    float c = dot(bnorm, normout); // ----- cosine
    float t = 1.0 - c;
    vec3 a = cross(bnorm, normout); // ----- axis
    float s = length(a); // ----- sine (depends on bnorm and normout being unit vectors)
    if (s > 0.0) a = normalize(a);
    normrot = mat4(
      t * a.x * a.x + c, t * a.x * a.y + a.z * s, t * a.x * a.z - a.y * s, 0.0,
      t * a.x * a.y - a.z * s, t * a.y * a.y + c, t * a.z * a.y + a.x * s, 0.0,
      t * a.x * a.z + a.y * s, t * a.y * a.z - a.x * s, t * a.z * a.z + c, 0.0,
      0.0, 0.0, 0.0, 1.0); // ----- vector mult for rotation about axis
    bumpcoordout = texcoord * ntiles;
  }
  
  if (shiny == 0.0) { // doubles as flag 0.0 for no reflection, negative means no lighting se .fs
    shinecoordout = vec2(0.0, 0.0);
  }
  else {
    vec3 inray = vertex - vec3(newmodel * vec4(eye, 1.0)); // ----- vector from the camera to this vertex
    if (length(inray) > 0.0) inray = normalize(inray); // ----- crash if normalize zero length vectors
    vec3 refl = reflect(inray, normout); // ----- reflection direction from this vertex
    vec3 horiz = cross(inray, vec3(0.0, 1.0, 0.0)); // ----- a 'horizontal' unit vector normal to the inray
    vec3 vert = cross(inray, vec3(1.0, 0.0, 0.0)); // ----- a 'vertical' unit vector normal to the inray
    float hval = dot(refl, horiz); // ----- component of the reflected ray along horizonal
    float vval = dot(refl, vert); // -----  componet of reflected ray along vertical
    float zval = dot(refl, -1.0 * inray); // ----- component of reflected ray in direction back to camera
    // ----- now work out the horizonal and vertical angles relative to inray and map them to range 0 to 1
    shinecoordout = vec2(clamp(0.5 - atan(hval, zval)/6.283185307, 0.0, 1.0), clamp(0.5 - atan(vval, zval)/6.283185307, 0.0, 1.0));
  }
  vec4 relPosn = newmodel_t * vec4(vertex,1.0);
  dist = length(relPosn);
  texcoordout = texcoord;
  gl_Position = relPosn;
}
