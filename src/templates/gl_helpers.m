/*
    Part of GLSL2FxPlug
    https://github.com/cappelnord/GLSL2FxPlug

    Code adapted from and inspired by the GLSLFxPlug Example in the FxPlug SDK.
*/

#include "gl_helpers.h"
#include <stdio.h>
#include <strings.h>

void getGLVersion(int *major, int *minor) {
    const char *version = (const char*) glGetString(GL_VERSION);
    if((version == NULL) || (sscanf(version, "%d.%d", major, minor) != 2)) {
        *major = 0;
        *minor = 0;
    }
}

void getGLSLVersion(int *major, int *minor) {
    int glMajor, glMinor;
    getGLVersion(&glMajor, &glMinor);
    
    *major = 0;
    *minor = 0;
    if(glMajor == 1) {
        const char *extensions = (const char*) glGetString(GL_EXTENSIONS);
        if((extensions != NULL) && (strstr(extensions, "GL_ARB_shading_language_100") != NULL)) {
            *major = 1;
            *minor = 0;
        }
    } else if(glMajor >= 2) {
        const char *version = (const char*) glGetString(GL_SHADING_LANGUAGE_VERSION);
        if( (version == NULL) || (sscanf(version, "%d.%d", major, minor) != 2)) {
            *major = 0;
            *minor = 0;
        }
    }
}

BOOL createShaderProgram(GLuint* program) {
    int glslMajor, glslMinor;
    
    getGLSLVersion(&glslMajor, &glslMinor);
    
    if(glslMajor <1) {
        return NO;
    }
    
    *program = glCreateProgram();
    if(!program) {
        return NO;
    }
    
    return YES;
}

BOOL linkShaderProgram(GLuint* program, char** shaderError) {
    GLint linked;
    
    glLinkProgram(*program);
    glGetProgramiv(*program, GL_LINK_STATUS, &linked);
    
    glValidateProgram(*program);
    int len;
    glGetProgramiv(*program, GL_INFO_LOG_LENGTH, &len);
    *shaderError = (char*) malloc((len+1) * sizeof(char));
    glGetProgramInfoLog(*program, len, &len, *shaderError);
    
    if(!linked) {
        glDeleteProgram(*program);
        *program = 0;
        return NO;
    }
    
    return YES;
}

BOOL loadShader(GLuint program, const char* src, GLenum type, char** shaderError) {
    GLuint shader;
    GLint compiled;
    
    shader = glCreateShader(type);
    glShaderSource(shader, 1, &src, NULL);
    glCompileShader(shader);
    glGetShaderiv(shader, GL_COMPILE_STATUS, &compiled);
    
    if(!compiled) {
        
        GLint len;
        glGetShaderiv(shader, GL_INFO_LOG_LENGTH, &len);
        *shaderError = malloc((len+1) * sizeof(char));
        glGetShaderInfoLog(shader, len, &len, *shaderError);
        
        if(shader) {
            glDeleteShader(shader);
            shader = 0;
        }
        return NO;
    }
    
    if(shader != 0) {
        glAttachShader(program, shader);
        glDeleteShader(shader);
        return YES;
    } else {
        return NO;
    }
}

BOOL loadVertexShader(GLuint program, const char* src, char** shaderError) {
    return loadShader(program, src, GL_VERTEX_SHADER, shaderError);
}

BOOL loadFragmentShader(GLuint program, const char* src, char** shaderError) {
    return loadShader(program, src, GL_FRAGMENT_SHADER, shaderError);
}
