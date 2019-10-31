from metakernel import MetaKernel
from IPython.display import HTML, Javascript

import re
import os
import sys
import subprocess
import tempfile

class ProcessingKernel(MetaKernel):
    implementation = 'Processing'
    implementation_version = '2.0'
    language = 'java'
    language_version = '2.2.1'
    language_info = {
        'mimetype': 'text/x-java',
        'name': 'java',
        'codemirror_mode': {
            "version": 2,
            "name": "text/x-java"
        },
        # 'pygments_lexer': 'language',
        # 'version'       : "x.y.z",
        'file_extension': '.java',
    }
    kernel_json = {
        "argv": [sys.executable,
                 "-m", "calysto_processing",
                 "-f", "{connection_file}"],
        "display_name": "Calysto Processing",
        "language": "java",
        "codemirror_mode": "java",
        "name": "calysto_processing",
    }
    banner = "Processing kernel - evaluates Processing programs"
    canvas_id = 0
    keywords = ["@pjs", "Array", "ArrayList", "HALF_PI",
                    "HashMap", "Object", "PFont", "PGraphics", "PI", "PImage",
                    "PShape", "PVector", "PrintWriter", "QUARTER_PI", "String",
                    "TWO_PI", "XMLElement", "abs", "acos", "alpha", "ambient",
                    "ambientLight", "append", "applyMatrix", "arc", "arrayCopy",
                    "asin", "atan", "atan2", "background", "beginCamera",
                    "beginRaw", "beginRecord", "beginShape", "bezier",
                    "bezierDetail", "bezierPoint", "bezierTangent",
                    "bezierVertex", "binary", "blend", "blendColor", "blue",
                    "boolean", "boolean", "box", "break", "brightness", "byte",
                    "byte", "camera", "case", "ceil", "char", "char", "class",
                    "color", "color", "colorMode", "concat", "constrain",
                    "continue", "copy", "cos", "createFont", "createGraphics",
                    "createImage", "createInput", "createOutput", "createReader",
                    "createWriter", "cursor", "curve", "curveDetail",
                    "curvePoint", "curveTangent", "curveTightness", "curveVertex",
                    "day", "default", "degrees", "directionalLight", "dist",
                    "double", "draw", "ellipse", "ellipseMode", "else",
                    "emissive", "endCamera", "endRaw", "endRecord", "endShape",
                    "exit", "exp", "expand", "extends", "false", "fill", "filter",
                    "final", "float", "float", "floor", "focused", "font", "for",
                    "frameCount", "frameRate", "frameRate", "frustum", "get",
                    "globalKeyEvents", "green", "height", "hex", "hint", "hour",
                    "hue", "if", "image", "imageMode", "implements", "import",
                    "int", "int", "join", "key", "keyCode", "keyPressed",
                    "keyPressed", "keyReleased", "keyTyped", "lerp", "lerpColor",
                    "lightFalloff", "lightSpecular", "lights", "line", "link",
                    "loadBytes", "loadFont", "loadImage", "loadPixels",
                    "loadShape", "loadStrings", "log", "long", "loop", "mag",
                    "map", "match", "matchAll", "max", "millis", "min", "minute",
                    "modelX", "modelY", "modelZ", "month", "mouseButton",
                    "mouseClicked", "mouseDragged", "mouseMoved", "mouseOut",
                    "mouseOver", "mousePressed", "mousePressed", "mouseReleased",
                    "mouseX", "mouseY", "new", "nf", "nfc", "nfp", "nfs",
                    "noCursor", "noFill", "noLights", "noLoop", "noSmooth",
                    "noStroke", "noTint", "noise", "noiseDetail", "noiseSeed",
                    "norm", "normal", "null", "online", "open", "ortho", "param",
                    "pauseOnBlur", "perspective", "pixels[]", "pmouseX",
                    "pmouseY", "point", "pointLight", "popMatrix", "popStyle",
                    "pow", "preload", "print", "printCamera", "printMatrix",
                    "printProjection", "println", "private", "public",
                    "pushMatrix", "quad", "radians", "random", "randomSeed",
                    "rect", "rectMode", "red", "requestImage", "resetMatrix",
                    "return", "reverse", "rotate", "rotateX", "rotateY",
                    "rotateZ", "round", "saturation", "save", "saveBytes",
                    "saveFrame", "saveStream", "saveStrings", "scale", "screen",
                    "screenX", "screenY", "screenZ", "second", "selectFolder",
                    "selectInput", "selectOutput", "set", "setup", "shape",
                    "shapeMode", "shininess", "shorten", "sin", "size", "smooth",
                    "sort", "specular", "sphere", "sphereDetail", "splice",
                    "split", "splitTokens", "spotLight", "sq", "sqrt", "static",
                    "status", "str", "stroke", "strokeCap", "strokeJoin",
                    "strokeWeight", "subset", "super", "switch", "tan", "text",
                    "textAlign", "textAscent", "textDescent", "textFont",
                    "textLeading", "textMode", "textSize", "textWidth", "texture",
                    "textureMode", "this", "tint", "translate", "triangle",
                    "trim", "true", "unbinary", "unhex", "updatePixels", "vertex",
                    "void", "while", "width", "year"]

    processing_functions = ["draw", "exit", "loop", "noLoop", "popStyle", "redraw", "setup", "size", "cursor", "frameRate", "noCursor", "binary", "boolean", "byte", "char", "float", "hex", "int", "str", "unbinary", "unhex", "join", "match", "matchAll", "nf", "nfc", "nfp", "nfs", "split", "splitTokens", "trim", "append", "arrayCopy", "concat", "expand", "reverse", "shorten", "sort", "splice", "subset", "for", "while", "else", "if", "switch", "arc", "ellipse", "line", "point", "quad", "rect", "triangle", "bezier", "bezierDetail", "bezierPoint", "bezierTangent", "curve", "curveDetail", "curvePoint", "curveTangent", "curveTightness", "box", "sphere", "sphereDetail", "ellipseMode", "noSmooth", "rectMode", "smooth", "strokeCap", "strokeJoin", "strokeWeight", "beginShape", "bezierVertex", "curveVertex", "endShape", "texture", "textureMode", "vertex", "loadShape", "shape", "shapeMode", "mouseClicked", "mouseDragged", "mouseMoved", "mouseOut", "mouseOver", "mousePressed", "mouseReleased", "keyPressed", "keyReleased", "keyTyped", "createInput", "loadBytes", "loadStrings", "open", "selectFolder", "selectInput", "link", "param", "status", "day", "hour", "millis", "minute", "month", "second", "year", "print", "println", "save", "saveFrame", "beginRaw", "beginRecord", "createOutput", "createReader", "createWriter", "endRaw", "endRecord", "saveBytes", "saveStream", "saveStrings", "selectOutput", "applyMatrix", "popMatrix", "printMatrix", "pushMatrix", "resetMatrix", "rotate", "rotateX", "rotateY", "rotateZ", "scale", "translate", "ambientLight", "directionalLight", "lightFalloff", "lightSpecular", "lights", "noLights", "normal", "pointLight", "spotLight", "beginCamera", "camera", "endCamera", "frustum", "ortho", "perspective", "printCamera", "printProjection", "modelX", "modelY", "modelZ", "screenX", "screenY", "screenZ", "ambient", "emissive", "shininess", "specular", "background", "colorMode", "fill", "noFill", "noStroke", "stroke", "alpha", "blendColor", "blue", "brightness", "color", "green", "hue", "lerpColor", "red", "saturation", "createImage", "image", "imageMode", "loadImage", "noTint", "requestImage", "tint", "blend", "copy", "filter", "get", "loadPixels", "set", "updatePixels", "createGraphics", "hint", "createFont", "loadFont", "text", "textFont", "textAlign", "textLeading", "textMode", "textSize", "textWidth", "textAscent", "textDescent", "abs", "ceil", "constrain", "dist", "exp", "floor", "lerp", "log", "mag", "map", "max", "min", "norm", "pow", "round", "sq", "sqrt", "acos", "asin", "atan", "atan2", "cos", "degrees", "radians", "sin", "tan", "noise", "noiseDetail", "noiseSeed", "random", "randomSeed"]

    special_keywords = {
        "@pjs": "pjs%20directive",
        "array": "array%20access",
        "[]": "array%20access",
        "[": "array%20access",
        "]": "array%20access",
        "()": "parentheses",
        "(": "parentheses",
        ")": "parentheses",
        "=": "assign",
        ",": "comma",
        "/*": "multiline%20comment",
        "*/": "multiline%20comment",
        ".": "dot",
        ";": "semicolon",
        "+=": "add%20assign",
        "+": "addition",
        "--": "decrement",
        "/": "divide",
        "/=": "divide%20assign",
        "++": "increment",
        "-": "minus",
        "%": "modulo",
        "*": "multiply",
        "*=": "multiply%20assign",
        "-=": "subtract%20assign",
        "&": "bitwise%20AND",
        "|": "bitwise%20OR",
        "<<": "left%20shift",
        ">>": "right%20shift",
        "==": "equality",
        ">": "greater%20than",
        ">=": "greater%20than%20or%20equal%20to",
        "!=": "inequality",
        "<": "less%20than",
        "<=": "less%20than%20or%20equal%20to",
        "&&": "logical%20AND",
        "!": "logical%20NOT",
        "||": "logical%20OR",
    }

    def get_usage(self):
        return "This is the Processing kernel based on Processingjs.org."

    def do_execute_direct(self, code):
        """%%processing - run contents of cell as a Processing script"""
        if code.strip() == "":
            return

        # first, we make sure it compiles

        in_directory = tempfile.mkdtemp()
        out_directory = tempfile.mkdtemp()
        filename = os.path.basename(in_directory) + ".pde"

        with open(os.path.join(in_directory, filename), "w") as fp:
            fp.write(code)

        processing_java = os.environ.get("PROCESSING_JAVA", "processing-java")
        cmd = [processing_java,
               "--sketch=%s" % in_directory,
               "--build", "--force",
               "--output=%s" % out_directory]
        try:
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except:
            self.Error("Unable to run command:", cmd)
            return
        stdout, stderr = [str(bin, encoding="utf-8") for bin in p.communicate()]

        if stderr:
            # 'other messages here...\nSketch.pde:8:0:8:0: The field Component.y is not visible\n'
            # sketch name:line start: col start: line end: col end: message
            # empty if successful
            for line in stderr.split("\n"):
                if line.strip() == "":
                    continue
                if line.startswith(filename):
                    tempname, line_start, col_start, line_end, col_end, message = line.split(":", 5)
                    message = message.strip()
                    code_lines = code.split("\n")
                    line_start = int(line_start)
                    line_end = int(line_end)
                    col_start = int(col_start)
                    if line_end == line_start:
                        line_end = line_start + 1
                    display_start = max(0, line_start - 3)
                    display_end = min(line_start + 3, len(code_lines))
                    if col_start:
                        self.Error("           " + (" " * (col_start - 1)) + "|")
                        self.Error("           " + (" " * (col_start - 1)) + "V")
                    self.Error(" Line     +" + ("-" * 75))
                    for line in range(display_start, display_end):
                        self.Error("%5s: %s | %s" % (line + 1, "->" if (line + 1) == line_start else "  ", code_lines[line]))
                    self.Error("          +" + ("-" * 75))
                    self.Error("")
                    self.Error("Compile error in line %d: %s" % (line_start, message))
                    #self.Print("Highlighted: %s %s %s %s" % (line_start - 2, 0, line_end - 2, 0))
                    self.Display(HTML("""
<style type="text/css">
      .styled-background { background-color: #ff7; }
</style>

<script>
if (typeof markedText !== 'undefined') {
        markedText.clear();
}
IPython.notebook.select_prev()
var cell = IPython.notebook.get_selected_cell();
markedText = cell.code_mirror.markText({line: %s, col: %s},
                                       {line: %s, col: %s},
                                       {className: "styled-background"});
cell.show_line_numbers(1)
IPython.notebook.select_next()
</script>
                    """ % (line_start - 2, 0, line_end - 2, 0)))
                else:
                    self.Error(line)
            return
        # else:
        # stdout
        # 'Finished.\n', if successful; '' otherwise

        self.canvas_id += 1
        repr_code = repr(code)
        if repr_code.startswith('u'):
            repr_code = repr_code[1:]
        env = {"code": repr_code,
               "id": self.canvas_id}
        code = """
<div id="canvas_div_%(id)s">
  <b>Sketch #%(id)s:</b><br/>
  <canvas id="canvas_%(id)s"></canvas><br/>
</div>
<div id="controls_div_%(id)s">
  <button id="run_button_%(id)s" onclick="startSketch('%(id)s');">
    <i class="fa fa-play-circle-o" style="size: 2em;"></i>
        Run
  </button>
  <button id="pause_button_%(id)s" onclick="pauseSketch('%(id)s');">
    <i class="fa fa-pause" style="size: 2em;"></i>
        Pause
  </button>
  <button id="setup_button_%(id)s" onclick="setupSketch('%(id)s');">
    setup()
  </button>
  <button id="draw_button_%(id)s" onclick="drawSketch('%(id)s');">
    draw()
  </button>
</div>
<b>Sketch #%(id)s state:</b> <span id="state_%(id)s">Loading...</span><br/>
<script>

function change_button(button, disable) {
    button.disabled = disable;
    if (disable) {
        button.style.color = "grey";
    } else {
        button.style.color = "black";
    }
}

function startSketch(id) {
    switchSketchState(id, true);
}

function pauseSketch(id) {
    switchSketchState(id, false);
}

function drawSketch(id) {
    var processingInstance = Processing.getInstanceById("canvas_" + id);
    if (processingInstance != undefined) {
        if (processingInstance.draw != undefined) {
            document.getElementById("state_" + id).innerHTML = "Drawing...";
            try {
                processingInstance.redraw();
                document.getElementById("state_" + id).innerHTML = "Drawing... done! Paused.";
                document.getElementById("state_" + id).style.color = "blue";
            } catch (e) {
                processingInstance.println(e.toString());
                document.getElementById("state_" + id).innerHTML = e.toString();
                document.getElementById("state_" + id).style.color = "red";
            }
        } else {
            document.getElementById("state_" + id).innerHTML = "No drawing() function. Paused.";
            document.getElementById("state_" + id).style.color = "blue";
        }
    } else {
        document.getElementById("state_" + id).innerHTML = "Error.";
        document.getElementById("state_" + id).style.color = "red";
    }
    change_button(document.getElementById("run_button_" + id), processingInstance.draw == undefined);
    change_button(document.getElementById("pause_button_" + id), true);
    change_button(document.getElementById("setup_button_" + id), processingInstance.setup == undefined);
    change_button(document.getElementById("draw_button_" + id), processingInstance.draw == undefined);
}

function setupSketch(id) {
    var processingInstance = Processing.getInstanceById("canvas_" + id);
    if (processingInstance != undefined) {
        if (processingInstance.setup != undefined) {
            document.getElementById("state_" + id).innerHTML = "Setting up...";
            try {
                processingInstance.setup();
                document.getElementById("state_" + id).innerHTML = "Setting up... done! Paused.";
                document.getElementById("state_" + id).style.color = "blue";
            } catch (e) {
                processingInstance.println(e.toString());
                document.getElementById("state_" + id).innerHTML = e.toString();
                document.getElementById("state_" + id).style.color = "red";
            }
        } else {
            document.getElementById("state_" + id).innerHTML = "No setup() function. Paused.";
            document.getElementById("state_" + id).style.color = "blue";
        }
    } else {
        document.getElementById("state_" + id).innerHTML = "Error.";
        document.getElementById("state_" + id).style.color = "red";
    }
    change_button(document.getElementById("run_button_" + id), processingInstance.draw == undefined);
    change_button(document.getElementById("pause_button_" + id), true);
    change_button(document.getElementById("setup_button_" + id), processingInstance.setup == undefined);
    change_button(document.getElementById("draw_button_" + id), processingInstance.draw == undefined);
}

function switchSketchState(id, on) {
    var processingInstance = Processing.getInstanceById("canvas_" + id);
    if (on) {
        document.getElementById("state_" + id).innerHTML = "Running...";
        document.getElementById("state_" + id).style.color = "green";
        change_button(document.getElementById("run_button_" + id), true);
        change_button(document.getElementById("pause_button_" + id), processingInstance.draw == undefined);
        change_button(document.getElementById("setup_button_" + id),  true);
        change_button(document.getElementById("draw_button_" + id), true);
        processingInstance.loop();  // call Processing loop() function
    } else {
        document.getElementById("state_" + id).innerHTML = "Paused.";
        document.getElementById("state_" + id).style.color = "blue";
        change_button(document.getElementById("run_button_" + id), processingInstance.draw == undefined);
        change_button(document.getElementById("pause_button_" + id), true);
        change_button(document.getElementById("setup_button_" + id), processingInstance.setup == undefined);
        change_button(document.getElementById("draw_button_" + id), processingInstance.draw == undefined);
        processingInstance.noLoop(); // stop animation, call noLoop()
    }
}

require([window.location.protocol + "//calysto.github.io/javascripts/processing/processing.js"], function () {
    var processingCode = %(code)s;
    var cc;
    var processingInstance;
    var has_error = false;

    try {
        cc = Processing.compile(processingCode);
    } catch (e) {
        console.log(e);
        cc = Processing.compile("println('" + e.toString() + "');");
        document.getElementById("state_%(id)s").innerHTML = e.toString();
        document.getElementById("state_%(id)s").style.color = "red";
        has_error = true;
    }
    if (cc != undefined) {
        try {
            processingInstance = new Processing("canvas_%(id)s", cc);
            processingInstance.println = window.jyp_println
        } catch (e) {
            console.log(e);
            cc = Processing.compile("println('" + e.toString() + "');");
            document.getElementById("state_%(id)s").innerHTML = e.toString();
            document.getElementById("state_%(id)s").style.color = "red";
            processingInstance = new Processing("canvas_%(id)s", cc);
            processingInstance.println = window.jyp_println
            has_error = true;
        }
    }
    if (processingInstance != undefined) {
        setTimeout(function () {
            // Canvas:
            if (processingInstance.externals.context === undefined) {
                document.getElementById("canvas_div_%(id)s").style.display = "none";
            }
        }, 100);
        // Controls:
        if (!(processingInstance.isRunning() && processingInstance.draw != undefined)) {
            document.getElementById("controls_div_%(id)s").style.display = "none";
        }
        if (processingInstance.draw != undefined) {
            if (!has_error) {
                document.getElementById("state_%(id)s").innerHTML = "Running...";
                document.getElementById("state_%(id)s").style.color = "green";
            }
            change_button(document.getElementById("run_button_%(id)s"), true);
            change_button(document.getElementById("pause_button_%(id)s"), false);
            change_button(document.getElementById("setup_button_%(id)s"),  true);
            change_button(document.getElementById("draw_button_%(id)s"), true);
        } else {
            if (!has_error) {
                document.getElementById("state_%(id)s").innerHTML = "Done.";
                document.getElementById("state_%(id)s").style.color = "blue";
            }
            change_button(document.getElementById("run_button_%(id)s"), true);
            change_button(document.getElementById("pause_button_%(id)s"), true);
            change_button(document.getElementById("setup_button_%(id)s"),  processingInstance.setup == undefined);
            change_button(document.getElementById("draw_button_%(id)s"), true);
        }
    } else {
        document.getElementById("canvas_div_%(id)s").style.display = "none";
        document.getElementById("controls_div_%(id)s").style.display = "none";
        if (!has_error) {
            document.getElementById("state_%(id)s").innerHTML = "Error.";
            document.getElementById("state_%(id)s").style.color = "red";
        }
        change_button(document.getElementById("run_button_%(id)s"), true);
        change_button(document.getElementById("pause_button_%(id)s"), true);
        change_button(document.getElementById("setup_button_%(id)s"),  true);
        change_button(document.getElementById("draw_button_%(id)s"), true);
    }
});

</script>
""" % env
        js = Javascript("""
        var component = document.getElementById("sketch_%(id)s");
        if (component != undefined)
            component.remove();
        component = document.getElementById("state_%(id)s");
        if (component != undefined)
            component.remove();
        component = document.getElementById("controls_div_%(id)s");
        if (component != undefined)
            component.remove();
        require([window.location.protocol + "//calysto.github.io/javascripts/processing/processing.js"], function() {
            // FIXME: Stop all previously running versions (?)
            var processingInstance = Processing.getInstanceById("canvas_%(id)s");
            if (processingInstance != undefined && processingInstance.isRunning())
                processingInstance.noLoop();
        });


        var output_area = this;
        // find my cell element
        var cell_element = output_area.element.parents('.cell');
        // which cell is it?
        var cell_idx = Jupyter.notebook.get_cell_elements().index(cell_element);
        // get the cell object
        var cell = Jupyter.notebook.get_cell(cell_idx);

        function jyp_print(cell, newline) {
            return function(message) {
                cell.get_callbacks().iopub.output({header: {"msg_type": "stream"},
                                                   content: {text: message + newline,
                                                             name: "stdout"}});
            }
        }
        window.jyp_println = jyp_print(cell, "\\n");
        window.jyp_print = jyp_print(cell, "");

        require([window.location.protocol + "//calysto.github.io/javascripts/processing/processing.js"], function() {
           Processing.logger.println = jyp_print(cell, "\\n");
           Processing.logger.print = jyp_print(cell, "");
        });


        """ % env)
        self.Display(js)
        html = HTML(code)
        self.Display(html)

    def get_completions(self, info):
        token = info["full_obj"]
        self.last_info = info
        return [command for command in set(self.keywords + self.processing_functions) if command.startswith(token)]

    def get_kernel_help_on(self, info, level=0, none_on_fail=False):
        expr = info["full_obj"]
        self.last_info = info
        url = None
        if expr in self.special_keywords:
            url = "http://processingjs.org/reference/%s/" % self.special_keywords[expr]
        elif expr in self.processing_functions:
            url = "http://processingjs.org/reference/%s_/" % expr
        elif expr in self.keywords:
            url = "http://processingjs.org/reference/%s/" % expr
        if url:
            try:
                import html2text
                import urllib
                try:
                    html = str(urllib.request.urlopen(url).read(), encoding="utf-8")
                except:
                    html = str(urllib.urlopen(url).read())
            except:
                return url
            visible_text = html2text.html2text(html)
            pattern = re.compile("(.*?)### ", re.DOTALL)
            visible_text = re.sub(pattern, "### ", visible_text, 1)
            return "Processing help from " + url + ":\n" + visible_text
        elif none_on_fail:
            return None
        else:
            return "Sorry, no available help for '%s'" % expr
