#version 330 core
layout(location=0) in vec3 aPos;
layout(location=1) in vec3 aNormal;
layout(location=2) in vec3 aColor;

// instance matrix (rows)
layout(location=3) in vec4 aM0;
layout(location=4) in vec4 aM1;
layout(location=5) in vec4 aM2;
layout(location=6) in vec4 aM3;

uniform mat4 uView;
uniform mat4 uProj;

out vec3 vNormal;
out vec3 vWorldPos;
out vec3 vColor;

void main() {
    mat4 model = mat4(aM0, aM1, aM2, aM3);
    vec4 worldPos = model * vec4(aPos,1.0);
    vWorldPos = worldPos.xyz;
    // normal matrix = inverse(transpose(model)) but for uniform scale or ortho, you can use upper‐left 3×3:
    vNormal = mat3(model) * aNormal;
    vColor  = aColor;
    gl_Position = uProj * uView * worldPos;
}