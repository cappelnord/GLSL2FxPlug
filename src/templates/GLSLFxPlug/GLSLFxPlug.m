${HEADER}

#import "${CLASSNAME}.h"
#include "gl_helpers.h"

${SHADER_SOURCE}


${PARAMETER_IDS}


@implementation ${CLASSNAME}

- (id)initWithAPIManager:(id)apiManager;
{
    _apiManager     = apiManager;
    _program_object = 0;
    
    char *err = NULL;
    
    // Now attempt to compile and link them
    BOOL cardSupportsGLSL = createShaderProgram(&_program_object);
    
    cardSupportsGLSL = cardSupportsGLSL && loadVertexShader(_program_object, vertexSource, &err);
    if(err != NULL) {
        printf("%s", err);
        free(err);
    }
    
    cardSupportsGLSL = cardSupportsGLSL && loadFragmentShader(_program_object, fragmentSource, &err);
    if(err != NULL) {
        printf("%s", err);
        free(err);
    }
    
    cardSupportsGLSL = cardSupportsGLSL && linkShaderProgram(&_program_object, &err);
    if(err != NULL) {
        printf("%s", err);
        free(err);
    }

    if (!cardSupportsGLSL)
    {
        [self release];
        self = nil;
    }
    
    return self;
}

- (void)dealloc
{
    // Clean up
    if (_program_object) 
    {
        glDeleteProgram(_program_object);
        _program_object = 0;
    }
    
    [super dealloc];
}

- (BOOL)variesOverTime
{
    return ${VARIES_OVER_TIME};
}


- (NSDictionary *)properties
{
    return [NSDictionary dictionaryWithObjectsAndKeys:
                [NSNumber numberWithBool: YES], kFxPropertyKey_SupportsRowBytes,
                [NSNumber numberWithBool: NO], kFxPropertyKey_SupportsR408,
                [NSNumber numberWithBool: NO], kFxPropertyKey_SupportsR4fl,
                [NSNumber numberWithBool: NO], kFxPropertyKey_MayRemapTime,
                NULL];
}

- (BOOL)addParameters
{
    id parmsApi;

    parmsApi = [_apiManager apiForProtocol:@protocol(FxParameterCreationAPI)];

    if ( parmsApi != NULL )
    {
        
        ${PARAMETERS}
        
        return YES;
    }
    else
    {
        return NO;
    }
}

- (BOOL)parameterChanged:(UInt32)parmId
{
    return YES;
}

- (BOOL)getOutputWidth:(NSUInteger *)width
                height:(NSUInteger *)height
             withInput:(FxImageInfo)inputInfo
              withInfo:(FxRenderInfo)renderInfo
{
    if ( width != NULL && height != NULL ) {
        *width  = inputInfo.width;
        *height = inputInfo.height;
        return YES;
    }
    else {
        return NO;
    }
}

- (BOOL)renderOutput:(FxImage *)outputImage
           withInput:(FxImage *)inputImage
            withInfo:(FxRenderInfo)renderInfo
{
    BOOL retval = YES;

    id parmsApi;
    parmsApi = [_apiManager apiForProtocol:@protocol(FxParameterRetrievalAPI)];

    ${REQUEST_APIS}

    if ( parmsApi != NULL ) {
        ${RETRIEVE_PARAMS}

        if ( [inputImage imageType] == kFxImageType_TEXTURE ) {
            double left, right, top, bottom;
            double tLeft, tRight, tTop, tBottom;
            FxTexture *inTex = (FxTexture *)inputImage;
            FxTexture *outTex = (FxTexture *)outputImage;

            glTexEnvi( GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE );

            [inTex getTextureCoords:&tLeft
                              right:&tRight
                             bottom:&tBottom
                                top:&tTop];

            [outTex getTextureCoords:&left
                               right:&right
                              bottom:&bottom
                                 top:&top];

            double tWidth = tRight - tLeft;
            double tHeight = tTop - tBottom;
            
            ${BIND_TEXTURES}
            
            if(_program_object) {
                glUseProgram(_program_object);
                ${SET_UNIFORMS}
            }
            
            glBegin(GL_QUADS);
            glTexCoord2f( tLeft, tBottom );
            glVertex2f( left, bottom );
            glTexCoord2f( tRight, tBottom );
            glVertex2f( right, bottom );
            glTexCoord2f( tRight, tTop );
            glVertex2f( right, top );
            glTexCoord2f( tLeft, tTop );
            glVertex2f( left, top );
            glEnd();
            
            // Clean up
            if(_program_object) {
                glUseProgram(0);
            }

            ${UNBIND_TEXTURES}
        }
        else {
            retval = NO;
        }
        ${CLEANUP}
    }
    else {
        retval = NO;
    }
    return retval;
}

- (BOOL)frameSetup:(FxRenderInfo)renderInfo
         inputInfo:(FxImageInfo)inputInfo
          hardware:(BOOL *)canRenderHardware
          software:(BOOL *)canRenderSoftware 
{
    *canRenderSoftware = NO;
    *canRenderHardware = YES;

    return YES;
}


- (BOOL)frameCleanup 
{
    return YES;
}

@end
