${HEADER}

#import <Foundation/Foundation.h>
#import <FxPlug/FxPlugSDK.h>

@interface ${CLASSNAME} : NSObject <FxFilter> {
    id<PROAPIAccessing> _apiManager;
    GLuint              _program_object;
}
@end
