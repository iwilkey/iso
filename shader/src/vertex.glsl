#version 330 core
layout(location = 0) in vec3 aPos;
layout(location = 1) in vec3 aColor;
layout(location=2) in vec4 aModelRow0;
layout(location=3) in vec4 aModelRow1;
layout(location=4) in vec4 aModelRow2;
layout(location=5) in vec4 aModelRow3;

uniform mat4 uView;
uniform mat4 uProj;
out vec3 vColor;

void main() {
    mat4 model = mat4(
        aModelRow0,
        aModelRow1,
        aModelRow2,
        aModelRow3
    );
    gl_Position = uProj * uView * model * vec4(aPos, 1.0);
    vColor      = aColor;
}
