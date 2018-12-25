A page with a button and two inputs.

Clicking the button or hitting enter when the second input is focused, runs `do_stuff`
which gets a reference to the input values and the button element using the `@inject` decorator.

`do_stuff` in turn, updates the button text.
