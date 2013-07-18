GLSL2FxPlug
===========

Automatic GLSL Shader 2 FxPlug Converter
----------------------------------------

GLSL is the OpenGL Shader Language, used to program the OpenGL Rendering Pipeline. It is used in 3D graphics but also for hardware accelerated image and video effects. GLSL2FxPlug lets you convert your GLSL fragment shaders into FxPlug plug-ins which can be used in Motion and supposedly in Final Cut Pro.

In general this isn't a very difficult to do, it's even in the FxPlug SDKs examples. GLSL2FxPlug does two things to make things easier and faster: First of all it automates all steps from Xcode project generation, up until installation of the plug-in. Second it uses a simple macro-style language to annotate meta information and to connect the GLSL uniform variables with parameters, which then are used for controlling and automating parameters.

GLSL2FxPlug wasn't designed for professional FxPlug developement, but as a tool for creative coders to easily bring their GLSL skills to Motion/Final Cut Pro.

### Installation

GLSL2FxPlug currently is designed to run in its own folder, so just clone this repository to your hard drive. In order to compile plug-ins you need to install:

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
* Run **glsl2fxplug.sh build/install** to compile and/or install your FxPlug
* Open Motion to test your new FxPlug plug-in (You might need to restart Motion for your plug-in or the changes to appear) 

### Usage

glsl2fxplug.sh is run in the Terminal. It takes two arguments:

```
./glsl2fxplug.sh [command] [classname]
```

Classnames must be valid C-style variable names (no whitespace, not starting with a number, ...). You can add .glsl2fxplug as an extension, if not it will be added automatically. If you ommit the command then *build* will be used as a default command.

The following commands are available:

* **template** generate a new template glsl2fxplug file
* **build** generates and builds a FxPlug from an existing glsl2fxplug file
* **install** same as build but also installs the plug-in to ~/Library/Plug-Ins/FxPlug/
* **test** doesn't generate a project, just parses file and runs GLSLTest
* **generate** generates a project but doesn't build it.
* **build-notest** generates and builds a project but does not run GLSLTest
* **install-notest** same as build-notest but also installs the plug-in.

### GLSL2FxPlug Files

GLSL2FxPlug files are standard text files, containing shader source cod and $-commands (lines starting with a $ sign and a command in capital letters). Commands are used to set meta-information, annotate sections or to add parameters.

Some commands have additional arguments, seperated by commas. Default values are used, if additional parameters aren't set. C-style comments (/* ... */) are safe to use to comment files.

*Example:*
```
$FLOAT Britghness, 1.0, 0.0, 2.0
/* A float uniform called Brightness with a default 
value of 1.0 and a parameter ranging from 0 to 2 */
```

#### Sections

**$VERTEX**

**$FRAGMENT**

The VERTEX and FRAGMENT commands mark the start of the vertex/fragment shaders. All text/parameters after the commands are added to the respective shader.
