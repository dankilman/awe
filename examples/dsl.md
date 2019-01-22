A page that demonstrates how to use the element DSL by calling the `new()` method with a DSL definition.
This example calls `new()` on the `page` instance, but in general, each element exposes the same functionally,
so complex element hierarchies can be added below it using different DSL definitions.

It also showcases many different element types supported by `awe`.

The following element types are used:

- tabs
- grids
- dividers
- cards
- texts
- tables

Element data is updated using API exposed by each element type.

In addition, the `divider` element is updated using the lower level `element.update_prop()` method which updates
the underlying props of the react component.

For more information on `awe`'s DSL, please refer to [DSL](https://awe-pages.readthedocs.io/en/latest/dsl.html).
