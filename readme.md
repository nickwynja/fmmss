- `make dev`: run in flask development server, accessible at http://localhost:5000
- `make build`: build the docker image
- `make up`: bring up with docker-compose, accessible at http://localhost:8080

## Form Markup

```html
<form action="https://api.litsub.com/1.0/subscribe" method="post">
  <label for="email">Email address:</label><br>
  <input type="text" name="email" value=""><br>
  <label for="name">Name:</label><br>
  <input type="text" name="name" value=""><br><br>
  <input type="hidden" name="list-writers" value="name@example.com" />
  <input type="hidden" name="success_redirect_url" value="https://litsub.com/subscribe-success.html">
  <input type="hidden" name="error_redirect_url" value="https://litsub.com/subscribe-error.html">
  <input type="checkbox" name="bottle_of_mead" value="1" style="display:none !important" tabindex="-1" autocomplete="off">
  <input type="submit" value="Join the List">
</form>
```
