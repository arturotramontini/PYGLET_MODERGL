// #version 330
// uniform vec2 u_resolution;
// uniform  vec3 color;
// out vec4 fragColor; // Colore del pixel
// void main() {
// //     vec4 d = vec4(distance(vec2(0)),1.0);

    

//  	vec2 st = gl_FragCoord.xy  / u_resolution;
//     float pct = 0.0;

//     // a. The DISTANCE from the pixel to the center
//     pct = distance(st,vec2(0.5));
//     d = vec4(vec3(pct),1.0);

//     fragColor = vec4(0.2, 0.6, 0.8, 1.0)+ vec4(color,1.0) ; // Colore blu-verde
// }


#version 330
uniform vec2 u_resolution;
uniform vec2 u_mouse;
uniform vec2 u_center1;
uniform vec2 u_center2;
uniform vec3 color;
uniform float u_raggio;
uniform float u_centerX;
uniform float u_centerY;
uniform float u_maxiter;
out vec4 fragColor;
void main() {


    float rd = u_raggio;
    float cpx = u_centerX ; //mouse.x;
    float cpy = u_centerY ; //mouse.y;
    float iter = 0;
    float maxiter = u_maxiter;

    // maxiter += 100;
    // rd  += 0.01;
    // cpx += (- 1.501) ; //mouse.x;
    // cpy += 0 ; //mouse.y;






    vec2 st = gl_FragCoord.xy  / u_resolution.xy;
    st -=  0.5 ; 
    st.x *= (u_resolution.x / u_resolution.y);

    vec2 mouse = (u_mouse / u_resolution);
    mouse  -= 0.5;
    mouse.x *= (u_resolution.x / u_resolution.y);




    vec2 center1 = (u_center1 / u_resolution);
    center1  -= 0.5;
    center1.x *= (u_resolution.x / u_resolution.y);

    vec2 center2 = (u_center2 / u_resolution);
    center2  -= 0.5;
    center2.x *= (u_resolution.x / u_resolution.y);


    vec3 col = color ; 
    float pct = 0.0;

    pct = distance(st,vec2(0,0)) ;


    vec3 d =  4 * vec3(pct);
    col -= d;

    col = color + vec3(0);    



    if ( ( abs(gl_FragCoord.x - u_resolution.x/2) < 1 ) && ( gl_FragCoord.x > u_resolution.x/2) ){
        col = vec3(.2,.2,.2);
    }
    if ( ( abs(gl_FragCoord.y - u_resolution.y/2) < 1 ) && ( gl_FragCoord.y > u_resolution.y/2) ){
        col = vec3(.2,.2,.2);
    }

    if ( ( abs(gl_FragCoord.y - 205) < 1 )  ){
        col = vec3(0,.1,0);
    }

    if ( ( gl_FragCoord.y > 210  )&&( gl_FragCoord.y < 210.6  )){
        col = vec3(0,.1,.1);
    }

    if ( (distance (vec2(gl_FragCoord.xy) , vec2(200,300)) < 1 )  ){
        col = vec3(.9,0,0);
    }
    if ( (distance (vec2(gl_FragCoord.xy) , vec2(300,200)) < 1 )  ){
        col = vec3(.5,0,0);
    }

    if(  
    (  distance (st , mouse) < 13/u_resolution.x) &&
    (  distance (st , mouse) > 12/u_resolution.x) 
    )
    {
        col = vec3(.8,0.8,0);
    }

    if  (  distance (st , center1) < 2/u_resolution.x)   {
        col = vec3(.1,0.8,0.5);
    }
    if  (  distance (st , center2) < 2/u_resolution.x)   {
        col = vec3(.1,0.5,0.8);
    }






    // float px = 0; //mouse.x;
    // float py = 0; //mouse.y;

    // float cx = st.x * 4 - 0.75 - px* 0.3;
    // float cy = st.y * 4 - py * 0.3;
    // float cx = st.x * rd - 0.75 - px* 0.3;
    // float cy = st.y * rd - py * 0.3;
 

    // maxiter += 26;
    // rd  += .8;
    // cpx += -1.758 ; //mouse.x;
    // cpy += 0 ; //mouse.y;    

    float temp = 0;
    float zxi = 0;
    float zyi = 0;
    float md = 0; //zx*zx+zy*zy;
    

    // =0.001 : per nascondere le righe dritte,, =1
    col *= 0.001;

    float cx = 0;
    float cy = 0;

    //-------------------------- per avere in verticale deve essere così come segue
    maxiter += 9;
    rd  += 3.7; 
    cpx += 0 ;  
    //-------------------------- per avere in verticale deve essere così come segue
    cpy += -0.54 ; 

    vec2 rp = u_mouse / u_resolution;
    cpx -= st.x * rp.x;
    cpy += st.y * rp.y;



    cx = st.y * rd + cpy ; 
    cy = st.x * rd + cpx ;
    //--------------------------

    // //-------------------------- per avere in orizzontale classico deve essere così come segue
    // maxiter += 6;
    // rd  += 2.46;
    
    // cpx += -0.57 ; 
    // cpy += 0 ; 



    // vec2 rp = u_mouse / u_resolution;
    // cpx += st.x * rp.x;
    // cpy += st.y * rp.y;
    
    // cx = st.x * rd + cpx ;
    // cy = st.y * rd + cpy ;
    // //--------------------------



    float zx = cx;
    float zy = cy;
    // float md = zx*zx+zy*zy;
    while (md < 400 && iter < maxiter){
        temp = zx*zx - zy*zy + cx;
        zy = 2 * zx * zy + cy;
        iter += 1;
        zx = temp;
        md = zx*zx+zy*zy;
        if (md < rd){
            zxi = zx;
            zyi = zy;
        }
    }
    float f = iter ; 
    float kv = 1.1 ;
    f = distance(vec2(zxi,zyi), vec2(0,0));
    f *= 1;
    f = max(f,1e-4);
    // f = abs(log(f)/log(10));
    // f = abs(log(f)/log(10));
    // f = abs(log(f)/log(10));
    // f = abs(log(f)/log(10));
    f = abs(log(f)/log(10));
    // f = abs(log(f)/log(10));
    // f = abs(log(f)/log(10));
    f = abs(log(f)/log(1.01));
    f = abs(log(f)/log(3.3));
    f = abs(log(f)/log(kv));
    // f = abs(log(f)/log(kv));
    // f = abs(log(f)/log(kv));
    // // f = abs(log(f)/log(kv));
    // f = abs(log(f)/log(kv));
    // f = abs(log(f)/log(kv));
    // f = abs(log(f)/log(kv));


    float col1 =  sin ( 31 * f) * 0.6 + 0.5;
    float col2 =  sin ( 2 * f) * 0.6 + 0.5;
    float col3 =  sin ( 3 * f) * 0.6 + 0.5;

    col1 *= 0.2;
    col2 *= 0.86;
    col3 *= 0.2;
    
    vec3 col4 = vec3(col1,col2,col3);

    col = 2.9*col + col4; //2 * iter / maxiter;

    // if (
    // ((int(gl_FragCoord.x) & 0x1) == 0) &&
    // ((int(gl_FragCoord.y) & 0x1) == 0) 
    // )
    //      col *= 1;
    // else
    //     col = vec3(0);

    fragColor = vec4(col, 1.0);
}