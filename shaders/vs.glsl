#version 400

layout (location = 0) in vec3 vertexPosition;
layout (location = 1) in vec3 vertexNormal;
layout (location = 2) in vec2 vertexTexCoord;

out vec3 color;
out vec3 position;
out vec3 normal;
out vec2 texCoord;

uniform mat4 modelViewMatrix;
uniform mat4 projectionMatrix;

// TODO
vec4 lightPosition = vec4(5.0, 5.0, 5.0, 0.0);
vec3 kd = vec3(1.0, 1.0, 1.0);
vec3 ld = vec3(1.0, 1.0, 1.0);
mat3 normalMatrix = mat3(transpose(inverse(modelViewMatrix)));

void main()
{
    vec3 tnorm = normalize(normalMatrix * vertexNormal);
    vec4 eyeCoords = modelViewMatrix * vec4(vertexPosition, 1.0);
    vec3 s = normalize(vec3(lightPosition - eyeCoords));
    color = ld * kd * max( dot(s, tnorm), 0.0 );

    texCoord = vertexTexCoord;
    normal = normalize(normalMatrix * vertexNormal);
    position = vec3(modelViewMatrix * vec4(vertexPosition, 1.0));

    gl_Position = projectionMatrix * modelViewMatrix * vec4(vertexPosition, 1.0);
}
