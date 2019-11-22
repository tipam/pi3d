// ----- boiler-plate code for fragment shader variable definition
#version 120
//precision mediump float;

uniform sampler2D tex0;
uniform sampler2D tex1;
uniform sampler2D tex2;
uniform vec3 unib[5];
// see docstring Buffer
uniform vec3 unif[20];
// see docstring Shape

varying float dist;
varying float fog_start;

//fragcolor