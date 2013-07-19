/*
    Part of GLSL2FxPlug
    https://github.com/cappelnord/GLSL2FxPlug
*/

#import "AppDelegate.h"
#include "gl_helpers.h"

${SHADER_SRC}

@implementation AppDelegate

- (void)dealloc
{
    [super dealloc];
}

- (void)applicationDidFinishLaunching:(NSNotification *)aNotification
{
    int glMajor, glMinor, glslMajor, glslMinor;
    
    getGLVersion(&glMajor, &glMinor);
    getGLSLVersion(&glslMajor, &glslMinor);
    
    printf("OpenGL version: %d.%d - GLSL version: %d.%d\n", glMajor, glMinor, glslMajor, glslMinor);
    
    if(glslMajor < 1) {
        printf("Error: GLSL version < 1\n");
        exit(EXIT_FAILURE);
    }
    
    GLuint program;
    BOOL success;
    
    success = createShaderProgram(&program);
    if(!success) {
        printf("Error: %s\n", gluErrorString(glGetError()));
        exit(EXIT_FAILURE);
    }
    
    char* shaderError = NULL;
    
    success = loadVertexShader(program, vertexSource, &shaderError);
    if(!success) {
        if(shaderError == NULL) {
            printf("Error in vertex shader: %s\n", gluErrorString(glGetError()));
        } else {
            printf("Error in vertex shader: %s\n", shaderError);
            free(shaderError);
            shaderError = NULL;
        }
        exit(EXIT_FAILURE);
    }
    
    success = loadFragmentShader(program, fragmentSource, &shaderError);
    if(!success) {
        if(shaderError == NULL) {
            printf("Error in fragment shader: %s\n", gluErrorString(glGetError()));
        } else {
            printf("Error in fragment shader: %s\n", shaderError);
            free(shaderError);
            shaderError = NULL;
        }
        exit(EXIT_FAILURE);
    }
    
    success = linkShaderProgram(&program, &shaderError);
    if(!success) {
        if(shaderError == NULL) {
            printf("Error in linking program: %s\n", gluErrorString(glGetError()));
        } else {
            printf("Error in linking program: %s\n", shaderError);
            free(shaderError);
            shaderError = NULL;
        }
        exit(EXIT_FAILURE);
    }
    
    exit(EXIT_SUCCESS);
}

@end
