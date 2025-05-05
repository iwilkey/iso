#version 330 core
in vec3 vNormal;
in vec3 vWorldPos;
in vec3 vColor;

uniform int  numDirLights;
struct DirLight {
    vec3 direction;
    vec3 color;
    float intensity;
};
uniform DirLight dirLights[4];

out vec4 FragColor;

void main(){
    vec3 N = normalize(vNormal);
    vec3 viewDir = normalize(-vWorldPos); // camera at origin
    // ambient + diffuse
    vec3 ambient = 0.1 * vColor;
    vec3 diffuse = vec3(0);
    for(int i=0; i<numDirLights; i++){
        vec3 L = normalize(-dirLights[i].direction);
        float d = max(dot(N,L), 0.0);
        diffuse += d * dirLights[i].color * dirLights[i].intensity * vColor;
    }
    FragColor = vec4(ambient + diffuse, 1.0);
}