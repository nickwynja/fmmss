# FMMSS

### Flask Mailman Static Subscribe

A Flask app running a `POST` API to handle subscribing to a [Mailman
3](https://gitlab.com/mailman/mailman) list from a static website. Designed to
attach to an existing
[`docker-mailman`](https://asynchronous.in/docker-mailman/) network, this app
will take requests to subscribe or unsubscribe users via the Python
`mailmanclient`.

## Form Markup

### Subscribe

*  `listEmail` - The email address you would like to subscribe to the list
*  `listName` - The name of the person you would like to subscribe to the list
*  `list-name` - Where `name` is an arbitrary string. `value` of `list-foo`
   should be the Mailman list name like `list@list.com`. Accepts multiple
   `list-name` fields in the form so you can optionally subscribe someone to
   multiple lists at one time
*  `success_redirect_url` - The URL you'd like the API to redirect to if the
   subscription was successful
*  `error_redirect_url` - The URL you'd like the API to redirect to if the subscription
   was unsuccessful
*  `email` - Honeypot field (see below for more details). This field should be
   hidden and is intended to prevent spam

#### Example

```html
<form action="https://fmmss.example.com/1.0/subscribe" method="post">
  <label for="listEmail">Email address:</label><br>
  <input type="text" name="listEmail" value=""><br>
  <label for="listName">Name:</label><br>
  <input type="text" name="name" value=""><br><br>
  <input type="hidden" name="list-writers" value="name@example.com" />
  <input type="hidden" name="success_redirect_url" value="https://example.com/subscribe-success.html">
  <input type="hidden" name="error_redirect_url" value="https://example.com/subscribe-error.html">
  <input class="ohnohoney" type="text" name="email" tabindex="-1" autocomplete="off">
  <input type="submit" value="Join the List">
</form>
```

See below for more details on the `ohnohoney` class.

### Unsubscribe

*  `email` - The address you'd like to unsubscribe
*  `list` - The list you'd like to unsubscribe the person from
*  `success_redirect_url` - The URL you'd like the API to redirect to if the
   unsubscription was successful
*  `error_redirect_url` - The URL you'd like the API to redirect to if the unsubscription
   was unsuccessful

## Spam Prevention with Honey Pot

To prevent bots from submitting spam subscriptions, I use a honeypot on the
subscription form. This isn't a required field but if you find yourselves with
swarming bees, the honey pot might help. The `name="email"` input attribute is
guaranteed to trap the bot into filling out the field. The `ohnohoney` class
visually hides the field though. So if the `POST` request contains information
in the `email` field, we can assume it's spam. To hide the honey pot field, add
the class `ohnohoney` and include the following CSS somewhere in your
stylesheet:

```css
.ohnohoney{
    opacity: 0;
    position: absolute;
    top: 0;
    left: 0;
    height: 0;
    width: 0;
    z-index: -1;
}
```
