.. _counter_tutorial:

Counter Tutorial
================

.. py:currentmodule:: malcolm.core

You should already know how to run up a Malcolm `process_` with some `Blocks
<block_>` that are each composed of `controller_` with `Parts <part_>`, and have
seen a Part that exposes a `method_`. Now we will look at a Part that exposes an
`attribute_` as well.

Let's take the example of a Counter. It contains:

- a writeable `attribute_` called ``counter`` which will keep the current
  counter value.
- a `method_` zero() which will set ``counter = 0``.
- a `method_` increment() which will set ``counter = counter + 1``.

The block definition in ``./malcolm/modules/demo/blocks/counter_block.yaml``
looks very similar to the hello_block example in the previous tutorial:

.. literalinclude:: ../../malcolm/modules/demo/blocks/counter_block.yaml
    :language: yaml

It creates the Methods and Attributes you would expect:

.. digraph:: counter_controllers_and_parts

    bgcolor=transparent
    node [fontname=Arial fontsize=10 shape=box style=filled fillcolor="#8BC4E9"]
    graph [fontname=Arial fontsize=11]
    edge [fontname=Arial fontsize=10 arrowhead=none]

    controller [shape=Mrecord label="{BasicController|mri: 'COUNTER'}"]
    cpart [shape=Mrecord label="{CounterPart|name: 'counter'}"]

    subgraph cluster_control {
        label="Control"
        labelloc="b"
        controller -> cpart
    }

    block [shape=Mrecord label="{Block|mri: 'COUNTER'}"]
    zero [shape=Mrecord label="{Method|name: 'zero'}"]
    increment [shape=Mrecord label="{Method|name: 'increment'}"]
    counter [shape=Mrecord label="{Attribute|name: 'counter'}"]
    health [shape=Mrecord label="{Attribute|name: 'health'}"]

    subgraph cluster_view {
        label="View"
        labelloc="b"
        block -> zero
        block -> increment
        block -> counter
        block -> health
    }

    {rank=same;controller block}

    controller -> health [style=dashed]
    cpart -> zero [style=dashed]
    cpart -> increment [style=dashed]
    cpart -> counter [style=dashed]
    controller -> block [arrowhead=vee dir=from style=dashed label=produces]

Creating Attributes in a Part
-----------------------------

Let's take a look at the definition of `CounterPart` in
``./malcolm/modules/demo/parts/counterpart.py`` now:

.. literalinclude:: ../../malcolm/modules/demo/parts/counterpart.py
    :language: python

Again, we start by subclassing `Part`, and we have decorated a couple
of functions with `method_takes`, but this time they don't take or
return any arguments, so the functions don't have a ``parameters`` argument.
The main difference to the Hello example is that we have implemented
:meth:`~Part.create_attribute_models` which expects us to create and yield any
`AttributeModel` instances we expect the Block to have.

.. note:: We are producing an `AttributeModel` rather than an `Attribute`.

    This is because the Attribute is a user facing View, with methods like
    :meth:`~Attribute.put_value`, while AttributeModel is a data centred model
    with methods like :meth:`~AttributeModel.set_value`. Each user gets their
    own `Attribute` view of a single underlying `AttributeModel` that holds the
    actual data.

In our example we yield:

- ``"counter"``: the name of the Attribute within the Block
- ``self.counter``: the AttributeModel instance
- ``self.counter.set_value``: the function that will be called when someone
  tries to "Put" to the Attribute, or None if it isn't writeable

To make the AttributeModel we first need to make a meta object. In our example
we want a ``float64`` `NumberMeta` as we want to demonstrate floating point
numbers. If our counter was an integer we could choose ``int32`` or ``int64``.
The actual AttributeModel is returned by the
:meth:`~VMeta.create_attribute_model` method of this meta.

In the two methods (zero and increment), we make use of the ``counter``
Attribute. We can get its value by using the :attr:`~AttributeModel.value`
attribute and set its value by calling the :meth:`~AttributeModel.set_value`
method. This method will validate the new value using the `VMeta` object we
passed in :meth:`~Part.create_attribute_models` and notify any interested subscribers
that something has changed.


Visualising the Block with the GUI
----------------------------------

.. highlight:: ipython

There is a basic PyQt GUI that ships with pymalcolm. We can use it to play
with this counter block and see how it works. Let's launch our demo again::

    [me@mypc pymalcolm]$ ./malcolm/imalcolm.py malcolm/modules/demo/DEMO-HELLO.yaml
    Loading...
    Python 2.7.3 (default, Nov  9 2013, 21:59:00)
    Type "copyright", "credits" or "license" for more information.

    IPython 2.1.0 -- An enhanced Interactive Python.
    ?         -> Introduction and overview of IPython's features.
    %quickref -> Quick reference.
    help      -> Python's own help system.
    object?   -> Details about 'object', use 'object??' for extra details.


    Welcome to iMalcolm.

    self.mri_list:
        ['localhost:8080']

    Try:
    hello = self.block_view("HELLO")
    print hello.greet("me")

    or

    gui(self.block_view("COUNTER"))

    or

    self.make_proxy("localhost:8080", "HELLO")
    print self.block_view("HELLO").greet("me")


    In [1]: gui(self.block_view("COUNTER"))

This will launch a GUI that lets us see what's going on:

.. image:: counter_1.png

If you try clicking the increment button a few times you should see the value
increase, the reset button should zero it and clicking on the counter value
should let you enter a number yourself. Notice that this value will also be
validated by the meta object we created, so you can enter ``34.5`` into the
counter value, but if you entered ``foo``, you will get a GUI that looks like
this:

.. image:: counter_2.png

And a message on the console::

    malcolm.core.request: Exception raised for request {"typeid": "malcolm:core/Put:1.0", "id": 13, "path": ["COUNTER", "counter", "value"], "value": "foo"}
    Traceback (most recent call last):
      File "./malcolm/../malcolm/core/controller.py", line 240, in _handle_request
        responses += handler(request)
      File "./malcolm/../malcolm/core/controller.py", line 269, in _handle_put
        result = put_function(request.value)
      File "./malcolm/../malcolm/core/attributemodel.py", line 51, in set_value
        self.set_value_alarm_ts(value, alarm, ts)
      File "./malcolm/../malcolm/core/attributemodel.py", line 61, in set_value_alarm_ts
        self.value = self.meta.validate(value)
      File "./malcolm/../malcolm/modules/builtin/vmetas/numbermeta.py", line 32, in validate
        cast = self._np_dtype(value)
    ValueError: could not convert string to float: foo

Conclusion
----------

This second tutorial has taken us through creating Attributes in Blocks and
showed us a little bit of the error checking that `VMeta` instances
give us. Now we have a CounterPart, we could combine it with the HelloPart
from the previous tutorial, creating a Controller with 2 Parts that has
counter and ``greet()`` functionality. In the next tutorial we will see how
we can use this composition to control multiple child blocks with one parent
Block.
