**Calysto Processing** is the merging of [ProcessingJS](http://processingjs.org/) with [Project Jupyter](http://jupyter.org/) (aka IPython). Processing Sketches are entered into Jupyter notebook cells, and even run in rendered notebooks. Sketches can be paused, and stepped one draw() at a time. 

Because Calysto Processing uses [MetaKernel](https://github.com/Calysto/metakernel/blob/master/README.rst), it has a fully-supported set of "magics"---meta-commands for additional functionality. A list of magics can be seen at [MetaKernel Magics](https://github.com/Calysto/metakernel/blob/master/metakernel/magics/README.md).

Calysto Processing in use:

* [CS110: Introduction to Computing](http://jupyter.cs.brynmawr.edu/hub/dblank/public/CS110%20Intro%20to%20Computing/2015/Syllabus.ipynb)
* [Video](https://www.youtube.com/watch?v=V4TzARh-ClY)

You can install Calysto Processing with:

```
pip3 install --upgrade calysto_processing --user
python3 -m calysto_processing install --user
```

or in the system kernels with:

```
sudo pip3 install --upgrade calysto_processing
python3 -m calysto_processing install --user
```

Next, install Processing 2 or 3 from https://processing.org/download/

You will need to make sure that you have installed and access to the `processing_java` command. Mac users will need to install it from Processing by selecting 'Install "processing_java"' under the Tools menu.

Finally, you need to set an environment variable with the location of processing-java, if it is not in your path. For example:

```
export PROCESSING_JAVA=/opt/processing-3.3.3/processing-java
```

Then, you can use it in the notebook with:

```
jupyter notebook
```

and then select `Calysto Processing` for a new notebook kernel.

Calysto Processing also has an enhancement: Tables, and some related functions:

```java
/* @pjs includeTable="true"; */

Table table;

void setup() {
    table = loadTable("test.csv", "header");
    println(table.getRowCount() + " total rows in table"); 
}

long findMax() {
    int retval = 0;
    for (TableRow row : table.rows()) {
        int pop = row.getInt("Population");
        if (pop > retval)
            retval = pop;
    }
    return retval;
}
```

Table-related classes and methods:

* loadTable(CSV_FILNAME, "header");
* Table class
* TableRow class
* table.rows() - returns iterator for use with for(TableRow row : table.rows()) {...}
* row.getInt(COLUMN_NAME)
* row.getString(COLUMN_NAME)
* row.getFloat(COLUMN_NAME)

See source for more details.

Example notebooks can be found in https://github.com/Calysto/calysto_processing/tree/master/notebooks

Requires:

* Jupyter
* Python3
* metakernel (installed with pip)
* calysto (installed with pip)

Calysto Processing supports:

* MetaKernel Magics
* All of ProcessingJS, plus pause/restart and stepper
