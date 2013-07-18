GLSL2FxPlug
===========

Automatic GLSL Shader to FxPlug Converter
----------------------------------------

GLSL is the OpenGL Shader Language, used to program the OpenGL Rendering Pipeline. It is used in 3D graphics but also for hardware accelerated image and video effects. GLSL2FxPlug lets you embed your GLSL fragment shaders into FxPlug plug-ins which can be used in Motion and supposedly in Final Cut Pro.

In general this isn't a very difficult to do, it's even in the FxPlug SDKs examples. GLSL2FxPlug does two things to make things easier and faster: First of all it automates all steps from Xcode project generation, up until installation of the plug-in. Second it uses a simple macro-style language to annotate meta information and to connect the GLSL uniform variables with parameters, which then are used for controlling and automating parameters.

GLSL2FxPlug wasn't designed for professional FxPlug developement, but as a tool for creative coders to easily bring their GLSL skills to Motion/Final Cut Pro.

### Installation

GLSL2FxPlug currently is designed to run in its own folder, so just clone this repository into a working directory. In order to compile plug-ins you need to install:

* Xcode (from Apple App Store)
* Xcode Command Line Tools (in Xcode->Preferences->Downloads)
* FxPlug SDK (Can be downloaded with a free Apple Developer account)

If glsl2fxplug.sh can't be executed you might need to make it executable.

```
chmod +x glsl2fxplug.sh
```

### General Usage

* Run **glsl2fxplug.sh template** to generate a .glsl2fxplug file template
* Edit FxPlug meta information (see Meta Information)
* Copy your GLSL shader source code into the .glsl2fxplug file (or write it from scratch)
* Replace all uniform variables with $-commands (see Parameters)
* Be sure to use sampler2DRect and not sampler2D
* Run **glsl2fxplug.sh build/install** to compile and/or install your FxPlug
* Open Motion to test your new FxPlug plug-in (You might need to restart Motion for your plug-in or the changes to appear) 

### Usage

glsl2fxplug.sh is run in the Terminal. It takes two arguments:

```
./glsl2fxplug.sh [command] [classname]
```

Classnames must be valid C-style variable names (no whitespace, not starting with a number, ...). You can add .glsl2fxplug as an extension, if not it will be added automatically. If you omit the command then *build* will be used as a default command.

The following commands are available:

* **template** generate a new template glsl2fxplug file
* **build** generates and builds a FxPlug from an existing glsl2fxplug file
* **install** same as build but also installs the plug-in to ~/Library/Plug-Ins/FxPlug/
* **test** doesn't generate a project, just parses file and runs GLSLTest
* **generate** generates a project but doesn't build it
* **build-notest** generates and builds a project but does not run GLSLTest
* **install-notest** same as build-notest but also installs the plug-in

### GLSL2FxPlug Files

GLSL2FxPlug files are standard text files, containing shader source cod and $-commands (lines starting with a $ sign and a command in capital letters). Commands are used to set meta-information, annotate sections or to add parameters.

Some commands have additional arguments, seperated by commas. Default values are used, if additional arguments aren't set. In the following documentation s/f/i/b are used to annotate the parameters type (String, Float, Integer, Boolean).

C-style comments (/* ... */) are safe to use to comment files.

*Example:*
```
$FLOAT Brightness, 1.0, 0.0, 2.0, 0.5, 1.5, 0.1, Total Brightness, 5
/* A float uniform called Brightness with a default 
value of 1.0, ranging from 0 to 2 and the slider ranging
from 0.5 to 1.5. Step value is 0.1. In a GUI the name is 
displayed as "Total Brightness" and the unique parameter
ID is 5. */
```

#### Sections


**$VERTEX** / **$FRAGMENT**

The **$VERTEX** and **$FRAGMENT** commands mark the start of the vertex/fragment shaders. All text/parameters after the commands are added to the respective shader.

#### Meta Information

#### Parameters

Instead of uniform variables you have to use parameter commands (which will be translated to standard GLSL uniforms). 

The first argument of a parameter command is always the variable name which will be used in GLSL. The last two arguments are usually a display name (which can contain spaces) which is displayed by the FxPlug (if not specified the variable name is used) and a unique parameter ID (integer) which is created automatically when omited.

The parameter ID is used to store parameter data. If you have finished developing your plug-in and want to use it in production it is wise to manually set the parameter ID, othwerwise it might change if you add new parameters and recompile.

***
**$FLOAT** [var_name]s, [default_value=0.0]f, [param_min=0.0]f, [param_max=1.0]f, [slider_min=0.0]f, [slider_max=1.0]f, [delta=0.1]f, *[display_name]s, [param_id]i*

Creates a **float** uniform variable *var_name* connected to a slider. **param_min/param_max** set the parameter range while **slider_min/slider_max** set only the range for the slider. **delta** is the step value a parameter is increase by using arrow up/down keys.

```
$FLOAT Brightness, 1.0, 0.0, 2.0, 0.5, 1.5
/* A float uniform called Brightness with a default 
value of 1.0, a parameter range from 0 to 2 but a 
slider range of just 0.5 to 1.5 */
```

***
**$INT** [var_name]s, [default_value=0]i, [param_min=0]i, [param_max=10]i, [slider_min=0]i, [slider_max=10]i, [delta=10]i, *[display_name]s, [param_id]i*

Basically the same as **$FLOAT** but creates an **int** uniform variable and an integer slider.

***
**$ANGLE** [var_name]s, [default_value=0.0]f, [param_min=0.0]f, [param_max=360.0]f, *[display_name]s, [param_id]i*

Creates two **float** uniforms connected to a rotary angle knob: **var_name** which contains the angle in degrees and **var_name**_rad which contains the angle in radians.

```
$ANGLE Angle, 0.0, -90.0, 90.0
/* Two float uniforms called Angle and Angle_rad with
a default value of 0.0, ranging from -90° to 90°. */
```

***
**$TOGGLE** [var_name]s, [default_value=True]b, *[display_name]s, [param_id]i*

Creates a **bool** uniform variable **var_name** connected to a checkbox. The default_value can be seit either by true/false or yes/no and is case insensitive.

```
$TOGGLE UseTexture, True
/* A bool uniform called UsedTexture ticked by default. */
```

***
**$POINT** [var_name]s, [default_x]f, [default_y]f, *[display_name]s, [param_id]i*

Creates a **vec2** uniform variable **var_name** connected to two sliders and a pointer control inside the canvas. Coordinates are in 0..1 range.

***
**$RGBA** [var_name]s, [default_red=0.0]f, [default_green=0.0]f, [default_blue=0.0]f, [default_alpha=1.0]f, *[display_name]s, [param_id]i*

Creates a **vec4** uniform variable **var_name** connected to a RGB color selector with aditional alpha slider. All values are in 0..1 range.

```
$RGBA Color, 1.0, 0.0, 0.0, 1.0
/* A vec4 uniform with solid red as default color. */
```

***
**$RGB** [var_name]s, [default_red=0.0]f, [default_green=0.0]f, [default_blue=0.0]f, *[display_name]s, [param_id]i*

Basically the same as **$RGBA** but creates a **vec3** uniform and has no alpha control.

***
**$IMAGE** [var_name]s, *[display_name]s, [param_id]i*

Creates a **sampler2DRect** uniform variable **var_name** connected to a drop-zone where you can put images, clips or groups from your timeline. Additionally the **vec2** uniform **var_name**_dim is created, containing the image dimensions in pixels.

```
$IMAGE ModImage
/* Creates a sampler2DRect uniform variable
called ModImage which can be sampled with texture2DRect */
```

***
**$FLOATPOPUP** [var_name]s, [default_index]i, {[name]s, [value]f}, [display_name]s, [param_id]i

Creates a **float** uniform variable **var_name** which is set by a popup menu. There can be as many **name** and **value** pairs as one likes. Because in this syntax it is impossible to distinguish between **name/value** pairs and **display_name/param_id** you have to explicitly specify **display_name** and **param_id**.

**default_index** starts with 0 and must be a valid index.

```
$FLOATPOPUP Value, 2, Nothing, 0.0, Half, 0.5, Full, 1.0, Value, 20
/* Creates a float uniform variable called Value and a
popup menu with 3 choices. The default selection is "Full" */
```

***
**$INTPOPUP** [var_name]s, [default_index]i, {[name]s, [value]i}, [display_name]s, [param_id]i

Basically the same as **$FLOATPOPUP** but creates an **int** uniform variable.

```
$INTPOPUP Channel, 0, Red, 0, Green, 1, Blue, 2, Color Channel, 21
/* Creates a int uniform variable called Channel and a
popup menu with 3 choices. The default selection is "Red" */
```

***
**$SUBGROUP** [var_name]s, *[display_name]s, [param_id]i*

Creates a collapsable subgroup in which all following parameters until the next **$ENDSUBGROUP** are put in. It doesn't create an uniform variable, unfortunately a valid **var_name** is still needed for book-keeping.

If **$SUBGROUP** is used when a subgroup is already open it will close it automatically and open a new one.

```
$SUBGROUP Group1, Group 1, 120
/* Creates a subgroup displayed with
"Group 1", with a unique paramater ID 120.
Group1 is only used for internal book-keeping. */
```

***
**$ENDSUBGROUP**

Closes a subgroup opened with **$SUBGROUP**. Only can be used when there's an open subgroup.

#### Other Uniforms

These uniform variables don't create a parameter, that's why only need a variable name and not a display name or parameter ID. They're used to get information from the host, clip and/or timeline.

***
**$INPUT** [var_name]s

Creates a **sampler2DRect** uniform variable **var_name** containing the image to be filtered.. Additionally the **vec2** uniform **var_name**_dim is created, containing the image dimensions in pixels.

***
**SCALE** [var_name]s

Creates a **vec2** uniform variable **var_name** containing the scale factor of the filter operation. This is relevant for rendering preview or half-quality images correctly when doing transformations on texture coordinates.

***
**$TIME** [var_name]s

Creates a **float** uniform variable **var_name** containing the current position of the timeline in seconds. Also creates a **float** uniform variable **var_name**_frame containing the same information in frames.

***
**$CLIPTIME** [var_name]s

Creates a **float** uniform variable **var_name** containing the current position of the filter clip duration in seconds. Also creates a **float** uniform variable **var_name**_frame containing the same information in frames.

***
**$CLIPDURATION** [var_name]s

Creates a **float** uniform variable **var_name** containing the duration of the filter clip in seconds. Also creates a **float** uniform variable **var_name**_frame containing the same information in frames.

***
**FPS** [var_name]s

Creates a **float** uniform variable **var_name** which contains the framerate of the timeline.

