precision mediump float;

varying vec2 texcoordout;

uniform sampler2D tex0;
uniform vec3 unif[20];    // hpe
//uniform float time =========> unif[16][0]
//uniform float fScale =======> unif[16][1]
//uniform float fOriginShift => unif[16][2]

// ---------------------------------------------------------------------------------
// original source found at: http://www.iquilezles.org/apps/shadertoy/
// Twist shaders was desgined by: http://www.iquilezles.org/apps/shadertoy/?p=Twist"
// Documentation and extention to Pi3D Peter Hess (01/2013)

void main(void) {

    // for better reading;
    float time =  unif[16][0];

    // the source of the texture color   
    vec2 uv_coord;   
  
    // compute the new position
    float a = atan(texcoordout.y, texcoordout.x);
    float r = length(texcoordout);

    // add time value to get a moving/modulated effect (the twist/warp)
    uv_coord.x = r - 0.25 * time;
    uv_coord.y = cos(a * 5.0 + 2.0 * sin(time + 7.0 * r)) ;

    // compute the new color from the given texture (This is the where the twisting is done)
    vec3 col =  (.5+.5*uv_coord.y) * texture2D(tex0,uv_coord).xyz;

    // set the new color
    gl_FragColor = vec4(col,1.0);
}

// removeme:  vec2 p = -1.0 + 2.0 * gl_FragCoord.xy / resolution.xy;
// removeme:  shotten muster vec2 p = texcoordout.xy * 10.0; <- 10 ist die Anzahl der Wellen (Scalierung???)
// removeme:  Pfauenfedern 2 vec2 p = gl_FragCoord.xy / texcoordout.xy;
// removeme:  Pfauenfedern vec2 p = -1.0 + 2.0 * gl_FragCoord.xy / texcoordout.xy;
