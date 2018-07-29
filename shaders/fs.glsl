#version 400

in vec3 color;
in vec3 position;
in vec3 normal;
in vec2 texCoord;

uniform sampler2D texture0;

layout( location = 0 ) out vec4 fragColor;

void main()
{
    vec4 texColor = texture(texture0, texCoord);

    fragColor = texColor * vec4(color, 1.0);
    fragColor = texColor;
}
