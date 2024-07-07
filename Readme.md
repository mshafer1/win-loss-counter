# win-loss-counter

Win-Loss-Counter is a websocket based widget (and control page) to sync 2 numbers (wins and losses).

## Why?

I have a friend that got into streaming and they wanted a way to display their current score (as it were) on their stream.
They also wanted to have their moderators or I be able to help them keep it in sync which made me lean towards a website based solution.

I opted to build it with websockets for the low-latency updates and to simplify the communication 
(i.e., rather than handling forms and having the front end pull, the server handles an event and publishes the updated score to all clients)

## License

Win-Loss-Counter is published under the [MIT License](LICENSE) and is completely free to use. If you would like to say thank you, you could 
<a href="https://buymeacoffee.com/mshafer1"><img src="images/bmc-button.png" style="max-height: 3ex;"></a>

## Hosting

### NOTE on self-hosting:

As built, this website requires a backend host to provide the socket that all instances of the frontend connect to.

According to source &nbsp;<sup>[2](#2)</sup>&nbsp;, SocketsBay.com offers this at no cost; however, I opted to run on my own hardware to avoid any snooping, privacy issues, or rate limits.

Utilizing that (or any other service) should be as simple as setting `VITE_DOMAIN=wss://socketsbay.com/wss/v2/100/{sockets_bay_api_key}` in `frontend\win-loss-counter\.env` before performing the build (**NOTE that this WILL expose your api key to all clients via source**)

### Deploying frontend with backend on self host

**Requirements**:
* Docker
* A domain name (for external access / nginx config)
* A way to have the domain access the server externally (not covered by this document)

To build and deploy on own server (without modifications):
1. Clone the repo `git clone https://github.com/mshafer1/win-loss-counter.git`

2. Create a .env file with the domain it will be served at (optional, used in step 4), the port to bind to, the secret key to use for flask (some random long string that you keep secret)

    ```bash
    #win-loss-counter/.env
    DOMAIN=widget.example.com
    PORT=2024
    FLASK_SECRET_KEY=B857BA2E-79C0-4817-833E-2340FFE0B484
    ```


3. CD into the project and build/start the docker image

    a. `cd win-loss-counter`

    b. `docker compose build`

    c. `docker compose up -d`

3. (optionally) use the included nginx site template for reverse proxy

    a. `cd hosting`

    b. `sudo make install` (requires ../.env lists the DOMAIN name that nginx should listen for)

    c. `sudo make install_ssl` to enable HTTPS (via certbot, which must also be installed for this command to work)
### A note on security

I deployed my instance using a [Cloudflare Zero Trust](https://developers.cloudflare.com/cloudflare-one/) tunnel configured so that `/` is world accessible, but `/control` is locked behind Cloudflare authentication. Because of this, there is not much security/auth setup in the app (only that if the user was able to get the `/control`, then consider them able to publish updates)

## Other resources

* <sup id="1">1</sup> [How to build a real-time Vue app with WebSockets](https://blog.logrocket.com/build-real-time-vue-app-websockets/) I started here for basic research
* <sup id="2">2</sup> [Vue 3+ WebSockets: How to build a realtime chat application in 15 minutes](https://medium.com/@ldanadrian/vue-3-websockets-how-to-build-a-realtime-chat-application-in-15-minutes-3b6a8ae5c08b) - read through this article as well
* <sup id="3">3</sup> Ultimately used the [vue-3-socket.io](https://www.npmjs.com/package/vue-3-socket.io) Node package to create/manage the socket on the frontend

  Most notably, this library expects the component to have a `sockets` object in the Vue component -> and the methods thre are the handlers for the socket (and the socket can be access via `this.$socket`)
* <sup id="4">4</sup> I chose to use [Flask-SocketIO](https://flask-socketio.readthedocs.io/en/latest/intro.html) to handle the backend (note, using library version 5.x meant having to force `socket.io-client` in the frontend up to 3.0)

* <sup id="5">5</sup> [Flask-Login](https://flask-login.readthedocs.io/en/latest/#configuring-your-application) is used to track which users have loaded the control page (and allow only them to send updates)
    * <sup id="5b">5b</sup> [How To Add Authentication to Your App with Flask-Login](https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login) provided a concrete, full example for how to integrate auth into the app
