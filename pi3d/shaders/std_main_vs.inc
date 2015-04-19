// ----- boiler-plate code for vertex shader to calculate light direction
//       vector and light strength factor

// NB previous define: modelviewmatrix, vertex, lightVector, unif, lightFactor, normout, normal

  vec4 relPosn = modelviewmatrix[0] * vec4(vertex, 1.0);
  
  if (unif[7][0] == 1.0) {                  // this is a point light and unif[8] is location
    lightVector = vec3(relPosn) - unif[8];
    lightFactor = pow(length(lightVector), -2.0);
    lightVector = normalize(lightVector);
  } else {                                  // this is directional light
    lightVector = normalize(unif[8]);
    lightFactor = 1.0;
  }
  lightVector.z *= -1.0;
  normout = normalize(vec3(modelviewmatrix[0] * vec4(normal, 0.0)));   
  vec3 bnorm = vec3(0.0, 0.0, 1.0); // ----- normal to original bump map sheet
  float c = dot(bnorm, normout); // ----- cosine
  float t = 1.0 - c;
  vec3 a = cross(bnorm, normout); // ----- axis
  float s = length(a); // ----- sine (depends on bnorm and normout being unit vectors)
  if (s > 0.0) a = normalize(a);
  // ----- vector mult for rotation about axis. This rather messy process is
  // done here in the vertex shader to orientate the light vector relative
  // to the normal map so that a simple dot product can be done with the
  // bump map value rather than having to rotation in the fragment shader.
  float txx = t * a.x * a.x, tyy = t * a.y * a.y, tzz = t * a.z * a.z,
        txy = t * a.x * a.y, txz = t * a.x * a.z, tyz = t * a.y * a.z,
        xs = a.z * s, ys = a.y * s, zs = a.z * s; // compiler might have noticed this optimisation, but anyway..
  lightVector = vec3(mat4(txx + c,  txy + zs, txz - ys, 0.0,
                          txy - zs, tyy + c,  tyz + xs, 0.0,
                          txz + ys, tyz - xs, tzz + c,  0.0,
                          0.0,      0.0,      0.0,      1.0) * vec4(lightVector, 0.0));
