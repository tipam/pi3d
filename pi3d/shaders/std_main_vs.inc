// ----- boiler-plate code for vertex shader to calculate light direction
//       vector and light strength factor

// NB previous define: modelviewmatrix, vertex, lightVector, unif, lightFactor, normout, normal

  vec4 relPosn = modelviewmatrix[0] * vec4(vertex, 1.0);
  
  if (unif[7][0] == 1.0) {                  // this is a point light and unif[8] is location
    lightVector = vec3(relPosn) - unif[8];
    lightFactor = pow(length(lightVector), -2.0);
    lightVector = normalize(lightVector);
    lightVector.z *= -1.0;
  } else {                                  // this is directional light
    lightVector = normalize(unif[8]);
    lightFactor = 1.0;
  }
  lightVector.z *= -1.0;
  // uvec, vvec are tangent and bitangent vectors at the vertex approx
  // lining up with the uv texture mapping. Because (0, 1, 0) is such a
  // common normal direction uvec is generated using just off vertical
  vec3 uvec = normalize(cross(normal, vec3(0.0003, -1.0, 0.0003)));
  vec3 vvec = normalize(cross(uvec, normal));
  normout = normalize(vec3(modelviewmatrix[0] * vec4(normal, 0.0)));   
  uvec = vec3(modelviewmatrix[0] * vec4(uvec, 0.0));
  vvec = vec3(modelviewmatrix[0] * vec4(vvec, 0.0));

  lightVector = vec3(mat4(uvec.x, vvec.x, -normout.x, 0.0,
                          uvec.y, vvec.y, -normout.y, 0.0,
                          uvec.z, vvec.z, -normout.z, 0.0,
                          0.0,    0.0,    0.0,        1.0) * vec4(lightVector, 0.0));
