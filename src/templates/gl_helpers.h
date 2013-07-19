/*
    Part of GLSL2FxPlug
    https://github.com/cappelnord/GLSL2FxPlug

    Code adapted from and inspired by the GLSLFxPlug Example in the FxPlug SDK.
*/

#ifndef __GL_HELPERS_H_
#define __GL_HELPERS_H_

#include <OpenGL/gl.h>
#include <OpenGL/glext.h>
#include <OpenGL/glu.h>

#include <Cocoa/Cocoa.h>

void getGLVersion(int *major, int *minor);
void getGLSLVersion(int *major, int *minor);

BOOL createShaderProgram(GLuint* program);
BOOL linkShaderProgram(GLuint* program, char** shaderError);
BOOL loadVertexShader(GLuint program, const char* src, char** shaderError);
BOOL loadFragmentShader(GLuint program, const char* src, char** shaderError);

#endif